from collections.abc import Collection, Iterable
from ipaddress import IPv4Address, IPv4Network
from typing import Union, Optional, Dict
from ipv4tree.utils import _get_binary_path_from_ipv4_addr


def prefixsize(n: int) -> int:
    return 2 ** (32 - n)


class IPv4TreeNode(Iterable):
    """
    Unit for IPv4Tree structure.
    """

    def __init__(self, key: Union[int, str],
                 prefixlen: int,
                 size: int = 1,
                 parent: Union['IPv4TreeNode', None] = None,
                 islast: bool = False,
                 info: Optional[Dict] = None):
        if parent is not None:
            parent.new_child(key, self)
        self._parent = parent
        self._children = [None, None]
        self._prefixlen = prefixlen
        self._prefix = "".join([parent.prefix, str(key)]) if parent is not None else str(key)
        self._size = size
        self._islast = islast
        self._info = info

    @property
    def parent(self) -> 'IPv4TreeNode':
        return self._parent

    @property
    def info(self) -> Optional[Dict]:
        if self._islast:
            return self._info
        return None

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def prefixlen(self) -> int:
        return self._prefixlen

    @property
    def prefixsize(self) -> int:
        return 2 ** (32 - self.prefixlen)

    def child(self, key: Union[int, str]) -> Union['IPv4TreeNode', None]:
        return self._children[int(key)]

    @property
    def children(self) -> list:
        return self._children

    def new_child(self, key: Union[int, str], node: Union['IPv4TreeNode', None]) -> None:
        self._children[int(key)] = node

    def update(self, prefixlen: int, size: int = 1) -> None:
        self._size += size
        if prefixlen > self._prefixlen:
            self._islast = True

    def fullness(self) -> float:
        """
        Get fullness rate for current node.
        :return: fullness rate
        """
        if self._prefixlen == 32:
            return 1.0
        if self._prefixlen == 31:
            return self._size / 2.0
        return self._size / (2.0 ** (32 - self._prefixlen))

    def __repr__(self) -> str:
        return str(self)

    def true_last_node(self):
        return self._children[0] is None and self._children[1] is None

    def aggregate(self, fullness: Union[int, float]) -> None:
        """
        Aggregate node: set last if fullness greater threshold.

        :param fullness: rate in (0, 1] interval
        """
        if self.fullness() >= fullness:
            self._islast = True

    def __iter__(self) -> Iterable:
        yield self
        if not self._islast:
            for child in self._children:
                if child is not None:
                    yield from iter(child)

    def __int__(self) -> int:
        from copy import deepcopy
        s = deepcopy(self._prefix)
        for _ in range(32 - self._prefixlen):
            s = "".join([s, "0"])
        return int(s, 2)

    def sizeof(self) -> int:
        if self.islast:
            return self._size if self._size > 0 else self.prefixsize

        size = 0
        for child in self._children:
            if child is not None:
                size += child.sizeof()

        return size

    def __str__(self) -> str:
        if self._prefixlen > 0:
            return "/".join([str(IPv4Address(int(self))),
                             str(self._prefixlen)])
        return "root"

    def _is_root(self) -> bool:
        return "root" == str(self)

    def network_address(self) -> IPv4Address:
        return IPv4Address(str(self).split('/')[0])

    @property
    def size(self) -> int:
        return self._size

    @property
    def islast(self) -> bool:
        return self._islast


class IPv4Tree(Collection):
    """
    Prefix tree for log(N) search IPv4 addresses and networks, and fast checks intree state.
    """

    def __init__(self) -> 'IPv4Tree':
        self._root = IPv4TreeNode(key=0,
                                  prefixlen=0,
                                  size=0)
        self._nodes = 1
        self._nodes_map = {}

    def _insert_node(self, prev: IPv4TreeNode, key: Union[int, str], size: int = 1, **kwargs) -> IPv4TreeNode:
        node = IPv4TreeNode(key=key,
                            prefixlen=prev.prefixlen + 1,
                            size=size,
                            parent=prev,
                            **kwargs)
        self._nodes += 1
        return node

    def __add__(self, other: 'IPv4Tree'):
        for node in other:
            if node.islast:
                self.insert(str(node))

        return self

    def sizeof(self, ip: Union[str, int, IPv4Address, IPv4Network]) -> int:
        net = IPv4Network(ip)
        node = self._root
        for n in _get_binary_path_from_ipv4_addr(net):
            node = node.child(n)
            if node is None:
                return 0

            if node.prefixlen == net.prefixlen:
                break

        return node.sizeof()

    def delete(self, ip: Union[str, int, IPv4Address, IPv4Network]) -> None:
        """
        Delete IPv4 address or network from tree
        :param ip: IPv4 address or network
        """
        net = IPv4Network(ip)
        if not self.intree(ip):
            raise ValueError('Network {} not in tree'.format(str(net)))

        size = self.sizeof(ip)
        node = self._root
        prev = node
        in_last = False
        for n in _get_binary_path_from_ipv4_addr(net):
            prev = node
            node = prev.child(n)
            inv_key = '1' if n == '0' else '0'
            inv_node = prev.child(inv_key)
            if prev.islast and not in_last:
                in_last = True

            if node is None:
                node = self._insert_node(prev, n, prefixsize(prev.prefixlen + 1))

            if inv_node is None:
                inv_node = self._insert_node(prev, inv_key, prefixsize(prev.prefixlen + 1))
                inv_node._islast = in_last

            prev._islast = False
            if node.prefixlen == net.prefixlen:
                break

        prev.new_child(n, None)
        if prev.true_last_node():
            prev._islast = True

        while prev is not None:
            prev.update(-1, -size)
            prev = prev.parent

    def intree(self, ip: Union[str, int, IPv4Address, IPv4Network]) -> bool:
        """
        Check address in tree.

        :param ip: IPv4 address or network
        :return: True if address or network exist in tree
        """
        ip = IPv4Network(ip)
        if ip in self:
            return True

        node = self._root
        for n in _get_binary_path_from_ipv4_addr(ip):
            prev = node
            node = prev.child(n)
            if node is None:
                return False
            if node.islast or node.prefixlen == ip.prefixlen:
                break
        return True

    def supernet(self, ip: Union[str, IPv4Address]) -> Optional[IPv4TreeNode]:
        """
        Return supernet for custom IPv4 address from IPv4Tree structure.

        :param ip: IPv4 Address, string or IPv4Address type
        :return: IPv4TreeNode or None if not exist in tree
        """
        ip = IPv4Network(ip)
        node = self._root
        for n in _get_binary_path_from_ipv4_addr(ip):
            prev = node
            node = prev.child(n)
            if node is None:
                return None
            if node.islast or node.prefixlen == ip.prefixlen:
                break
        return node

    def insert_node(self, new_node: IPv4TreeNode) -> None:
        """
        Insert IPv4 address or network in IPv4Tree structure.

        :param ip: IPv4 address or network
        :param kwargs: custom parameters for your nodes.
        """
        ip = IPv4Network(str(new_node))
        if ip in self:
            return

        size = new_node.size
        node = self._root
        self._root.update(-1, size)
        was_insert = False
        for n in _get_binary_path_from_ipv4_addr(ip):
            prev = node
            node = prev.child(n)
            if node is None:
                node = self._insert_node(prev, n, size)
                was_insert = True
            else:
                node.update(node.prefixlen, size)

            if node.prefixlen == ip.prefixlen:
                new_node._parent = prev
                node = new_node
                break

        prev.new_child(n, new_node)
        if not was_insert:
            if node.prefixlen != ip.prefixlen:
                # is supernet
                excess = size
            else:
                excess = node.size - size
            while node is not None:
                node.update(-1, -excess)
                node = node.parent
        else:
            # new node in last level
            self._nodes_map[ip] = node

    def insert(self, ip: Union[str, int, IPv4Address, IPv4Network], **kwargs) -> None:
        """
        Insert IPv4 address or network in IPv4Tree structure.

        :param ip: IPv4 address or network
        :param kwargs: custom parameters for your nodes.
        """
        ip = IPv4Network(ip)
        if ip in self:
            return

        size = ip.num_addresses
        node = self._root
        self._root.update(-1, size)
        was_insert = False
        for n in _get_binary_path_from_ipv4_addr(ip):
            prev = node
            node = prev.child(n)
            if node is None:
                node = self._insert_node(prev, n, size, **kwargs)
                was_insert = True
            else:
                node.update(node.prefixlen, size)

            if node.islast:
                # try insert for subnetwork of exist in tree
                break

            if node.prefixlen == ip.prefixlen:
                # try insert for supernetwork?
                break

        node._islast = True
        if not was_insert:
            if node.prefixlen != ip.prefixlen:
                # is supernet
                excess = size
            else:
                excess = node.size - size
            while node is not None:
                node.update(-1, -excess)
                node = node.parent
        else:
            # new node in last level
            self._nodes_map[ip] = node

    def fake_insert(self, ip: Union[str, int, IPv4Address, IPv4Network], **kwargs) -> None:
        """
        Fake insert IPv4 address or network in IPv4Tree structure (path created for multiprocessing usage).

        :param ip: IPv4 address or network
        :param kwargs: custom parameters for your nodes.
        """
        ip = IPv4Network(ip)
        size = ip.num_addresses
        node = self._root
        self._root.update(-1, size)
        was_insert = False
        for n in _get_binary_path_from_ipv4_addr(ip):
            prev = node
            node = prev.child(n)
            if node is None:
                node = self._insert_node(prev, n, size, **kwargs)
                was_insert = True

            if node.prefixlen == ip.prefixlen:
                # try insert for supernetwork?
                break

        if not was_insert:
            if node.prefixlen != ip.prefixlen:
                # is supernet
                excess = size
            else:
                excess = node.size - size
            while node is not None:
                node.update(-1, -excess)
                node = node.parent

    def fast_insert(self, ip: Union[str, int, IPv4Address, IPv4Network], **kwargs) -> None:
        """
        Insert IPv4 address or network in IPv4Tree structure.
        ATTENTION! Has no updates for size!

        :param ip: IPv4 address or network
        :param kwargs: custom parameters for your nodes.
        """
        ip = IPv4Network(ip)
        if ip in self:
            return

        node = self._root
        was_insert = False
        for n in _get_binary_path_from_ipv4_addr(ip):
            prev = node
            node = prev.child(n)
            if node is None:
                node = self._insert_node(prev, n, **kwargs)
                was_insert = True

            if node.islast:
                # try insert for subnetwork of exist in tree
                break

            if node.prefixlen == ip.prefixlen:
                # try insert for supernetwork?
                break

        node._islast = True
        if was_insert:
            # new node in last level
            self._nodes_map[ip] = node

    def __contains__(self, ipv4: Union[str, int, IPv4Address, IPv4Network]) -> bool:
        return IPv4Network(ipv4) in self._nodes_map.keys()

    def __iter__(self) -> Iterable:
        return iter(self._root)

    def __len__(self) -> int:
        return self._root.size

    def __getitem__(self, ipv4: Union[str, int, IPv4Address, IPv4Network]) -> IPv4TreeNode:
        net = IPv4Network(ipv4)
        node = self._root
        for n in _get_binary_path_from_ipv4_addr(net):
            node = node.child(n)
            if node is None or node.prefixlen == net.prefixlen:
                break
        return node

    def aggregate(self, fullness: Union[int, float]) -> None:
        """
        Aggregate networks by fullness rate.

        :param fullness: float in (0, 1] interval.
        """
        for node in self:
            node.aggregate(fullness)

    def last_assignment(self, prefixlen: int = 32, islast: bool = False) -> None:
        """
        Default values undo 'aggregate' method
        """
        for node in self:
            if node.prefixlen < prefixlen:
                node._islast = islast

    def __repr__(self) -> str:
        prefixlens = {}
        last_nodes = 0
        for node in self:
            prefixlen = str(node.prefixlen)
            if prefixlen not in prefixlens.keys():
                prefixlens[prefixlen] = 1
            else:
                prefixlens[prefixlen] += 1

            if node.islast:
                last_nodes += 1

        return str(prefixlens) + "\nTotal nodes: {}\nSize: {}" \
                                 "\nLast nodes: {}".format(self._nodes,
                                                           self._root.size,
                                                           last_nodes)


class CIDRTree(IPv4Tree):
    """
    The prefix tree special for CIDR matching based on IPv4TRee.

    Insert: ignore already existed node for insert in tree.
    Supernet: search all last nodes and return node with largest prefixlen.
    """

    def insert(self, ip: Union[str, int, IPv4Address, IPv4Network], **kwargs) -> None:
        """
        Insert IPv4 address or network in IPv4Tree structure.
        IMPORTANT! Insert are ignore exists networks in path!

        :param ip: IPv4 address or network
        :param kwargs: custom parameters for your nodes.
        """
        ip = IPv4Network(ip)
        if ip in self:
            return

        size = ip.num_addresses
        node = self._root
        self._root.update(-1, size)
        was_insert = False
        for n in _get_binary_path_from_ipv4_addr(ip):
            prev = node
            node = prev.child(n)
            if node is None:
                node = self._insert_node(prev, n, size, **kwargs)
                was_insert = True
            else:
                node.update(node.prefixlen, size)

            if node.prefixlen == ip.prefixlen:
                # try insert for supernetwork?
                break

        node._islast = True
        if not was_insert:
            if node.prefixlen != ip.prefixlen:
                # is supernet
                excess = size
            else:
                excess = node.size - size
            while node is not None:
                node.update(-1, -excess)
                node = node.parent
        else:
            # new node in last level
            self._nodes_map[ip] = node

    def fast_insert(self, ip: Union[str, int, IPv4Address, IPv4Network], **kwargs) -> None:
        """
        Insert IPv4 address or network in IPv4Tree structure.
        ATTENTION! Has no updates for size!

        :param ip: IPv4 address or network
        :param kwargs: custom parameters for your nodes.
        """
        ip = IPv4Network(ip)
        if ip in self:
            return

        node = self._root
        was_insert = False
        for n in _get_binary_path_from_ipv4_addr(ip):
            prev = node
            node = prev.child(n)
            if node is None:
                node = self._insert_node(prev, n, **kwargs)
                was_insert = True

            if node.prefixlen == ip.prefixlen:
                # try insert for supernetwork?
                break

        node._islast = True
        if was_insert:
            # new node in last level
            self._nodes_map[ip] = node

    def supernet(self, ip: Union[str, IPv4Address, IPv4Network]) -> Optional[IPv4TreeNode]:
        """
        Return supernet for custom IPv4 address from IPv4Tree structure.
        IMPORTANT! Return subnet in tree with largest prefixlen!

        :param ip: IPv4 Address, string or IPv4Address type
        :return: IPv4TreeNode or None if not exist in tree
        """
        ip = IPv4Network(ip)
        node = self._root

        last_nodes = []
        for n in _get_binary_path_from_ipv4_addr(ip):
            prev = node
            node = prev.child(n)
            if node is None:
                break

            if node.islast:
                last_nodes.append(node)

            if node.prefixlen == ip.prefixlen:
                last_nodes.append(node)
                break

        return last_nodes[-1] if last_nodes else None
