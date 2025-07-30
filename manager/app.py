import redis, json, time

r = redis.Redis(host='redis', port=6379)
r.delete('results')

# tasks
tasks = [{"task_id": task, "range": ((task-2)*10 + 2, ((task-1)*10 + 2))} for task in range(2, 12)]
print(f"TASKS: {tasks}")
print(f"{len(tasks)} tasks.")

start_time = time.time()
for task in tasks:
    r.lpush('task_queue', json.dumps(task))
while r.llen('results') < len(tasks):
    time.sleep(0.2)
end_time = time.time()
print(f"✅ All tasks completed in {end_time - start_time:.2f} seconds.")