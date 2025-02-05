# 問題：次の操作をほぼ O(1) で実現するデータ構造を考える
# 与えられた <URL, Web ページ> があるかないかを検索
# もしない場合、キャッシュ内で一番古い <URL, Web ページ> を捨てて、かわりに与えられた <URL, Web ページ> を追加する
# ヒント：
# ハッシュテーブルだけだと順序を管理できないので、別のデータ構造を組み合わせて、X 個の <URL, Web ページ> をアクセスされた順に取り出せるようにする😀

class Node_List:
    def init(self,key,value):
        self.key = key 
        self.value = value 
        self.prev = None
        self.next = None
    
class linked_list:
    def init(self):
        self.head = Node_List(0,0)
        self.tail = Node_List(0,0)
        self.head.prev = self.head #テイルの前をヘッドに設定
        self.head.next = self.tail #ヘッドの次をテイルに設定
    
    
    def add(self, node: Node_List) -> None:
        node.prev = self.head #新しいノードの前をヘッドに設定
        node.next = self.head.next #新しいノードの次をヘッドの次に設定
        self.head.prev = node #ヘッドの次を新しいノードに設定
        self.head.next.prev = node #元のヘッドの次のノードの前を新しいノードに設定

    
    def remove(self, node: Node_List) -> None:
        node.prev.next = node.next #削除するノードの前のノードの次を削除するノードの次に設定
        node.next.prev = node.prev #削除するノードの次のノードの前を削除するノードの前に設定


    def move_to_head(self, node: Node_List) -> None:
        self.remove(node)
        self.add(node)

def calculate_hash(key):
    assert type(key) == str
    hash = 0
    prime = 31 #素数
    modulus = 2**32 #係数
    for i, char in enumerate(key):
        hash = (hash * prime + ord(char)) % modulus
    return hash

class Item:
    def __init__(self, key, value, next):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next
        
class HashTable:


    def __init__(self):

        self.bucket_size = 97
        self.buckets = [None] * self.bucket_size
        self.item_count = 0

    def put(self, key, value):
        assert type(key) == str
        self.check_size() # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                item.value = value
                return False
            item = item.next
        new_item = Item(key, value, self.buckets[bucket_index])
        self.buckets[bucket_index] = new_item
        self.item_count += 1
        return True

    def get(self, key):
        assert type(key) == str
        self.check_size() # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                return (item.value, True)
            item = item.next
        return (None, False)

    def delete(self, key):
        assert type(key) == str 
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        prev = None
        while item:
            if item.key == key:
                if prev != None:
                    prev.next = item.next
                else:
                    self.buckets[bucket_index] = item.next
                self.item_count -= 1
                return (item.value, True)
            prev = item
            item = item.next
        return (None, False)

    def size(self):
        return self.item_count

    def check_size(self):
        assert (self.bucket_size < 100 or
                self.item_count >= self.bucket_size * 0.3)
        
    def rehash(self):#再ハッシュ
        new_bucket_size = self.bucket_size * 2
        new_buckets = [None] * new_bucket_size

        for i in range(self.bucket_size):
            item = self.buckets[i]
            while item:
                #ハッシュ値を再計算し、新しいバケットリスト内でのインデックスを決定
                new_bucket_index = calculate_hash(item.key) % new_bucket_size 
                next_item = item.next
                item.next = new_buckets[new_bucket_index]
                new_buckets[new_bucket_index] = item
                item = next_item

        self.bucket_size = new_bucket_size
        self.buckets = new_buckets
        
class URL_Cache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = HashTable()
        self.linked_list = linked_list()

    def get(self, key: str) -> str:
        value = self.cache.get(key)
        found = self.cache.get(key)
        if not found:
            return None
        node = value
        self.linked_list.move_to_head(node)
        return node.value

    def put(self, key: str, value: str) -> None:
        node = self.cache.get(key)
        found = self.cache.get(key)
        if found:
            node.value = value
            self.linked_list.move_to_head(node)
        else:
            new_node = Node_List(key, value)
            self.cache.put(key, new_node)
            self.linked_list.add(new_node)

            if self.cache.size() > self.capacity:
                tail_node = self.linked_list.remove_tail()
                if tail_node:
                    self.cache.delete(tail_node.key)