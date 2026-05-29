import json
d=json.load(open('/home/thinhnh39/ai-103/questions.json'))
print('Total:', d['metadata']['totalQuestions'])
print()
q1 = d['questions'][0]
print(f"Q1 label: {q1['label']}")
print(f"Q1 prompt first 150: {q1['prompt'][:150]}")
print(f"Q1 options: {len(q1['options'])}")
print(f"Q1 answer: {q1['answer']}")
print()
q66 = d['questions'][65]
print(f"Q66 label: {q66['label']}")
print(f"Q66 prompt first 150: {q66['prompt'][:150]}")
print(f"Q66 images: {q66['questionImages'][:1]}")
print(f"Q66 answer: {q66['answer']}")
print(f"Q66 explanationImages count: {len(q66['explanationImages'])}")
print()
q100 = d['questions'][99]
print(f"Q100 label: {q100['label']}")
print(f"Q100 type: {q100['type']}")
print(f"Q100 answer: {q100['answer']}")
