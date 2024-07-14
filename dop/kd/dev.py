import heapq

# 创建一个空的优先队列
priority_queue = []

# 向优先队列中添加元素
heapq.heappush(priority_queue, ((3, -3), 'Task 3'))
heapq.heappush(priority_queue, ((3, -1), 'Task 1'))
heapq.heappush(priority_queue, ((3, -1), 'Task 1'))
heapq.heappush(priority_queue, ((3, -2), 'Task 2'))


print(priority_queue)
heapq.heapify(priority_queue)
print(priority_queue)
# 从优先队列中取出元素
while priority_queue:
    priority, task = heapq.heappop(priority_queue)
    print(f'Priority: {priority}, Task: {task}')
    # res = heapq.nsmallest(10, priority_queue)
    # print(res)
    # break
print(priority_queue)