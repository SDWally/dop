# K个有序链表合并

## 思路

1. 暴力
2. 分治（两两合并后再合并）
3. 优先队列

## 示例（基于优先队列）

    class Solution:
        def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
            import heapq
            dummy = ListNode(0)
            p = dummy
            head = []
            for i in range(len(lists)):
                if lists[i] :
                    heapq.heappush(head, (lists[i].val, i))
                    lists[i] = lists[i].next
            while head:
                print(head)
                val, idx = heapq.heappop(head)
                
                p.next = ListNode(val)
                p = p.next
                if lists[idx]:
                    heapq.heappush(head, (lists[idx].val, idx))
                    lists[idx] = lists[idx].next
            return dummy.next
            
           
- heapq.heappush 会一直保持 head列表的有序性
- heapq.heappop 会pop出最小值