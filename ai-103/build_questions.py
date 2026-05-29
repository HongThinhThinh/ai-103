import json, os, re

# ============================================================
# SAMPLE 1: AI-103.md (65 questions) with answers from foundry_practice_exam_answers.json
# ============================================================
base = "/home/thinhnh39/ai-103"

with open(os.path.join(base, "AI-103.md"), encoding="utf-8") as f:
    md_content = f.read()

with open(os.path.join(base, "foundry_practice_exam_answers.json"), encoding="utf-8") as f:
    answers_data = json.load(f)
answers_map = {q["id"]: q for q in answers_data["questions"]}

# Parse AI-103.md into individual questions
# Split by "### Question X"
question_blocks = re.split(r'(?=^### Question \d+)', md_content, flags=re.MULTILINE)
question_blocks = [b.strip() for b in question_blocks if b.strip().startswith("### Question")]

print(f"Sample 1: Parsed {len(question_blocks)} questions from AI-103.md")

sample1 = []
for block in question_blocks:
    # Extract question number
    m = re.match(r'### Question (\d+)', block)
    if not m:
        continue
    qnum = int(m.group(1))

    # Get the full text after the header line
    lines = block.split('\n')
    # Remove the header line
    body = '\n'.join(lines[1:]).strip()

    # Get answer info
    ans_info = answers_map.get(qnum, {})

    # Parse options from markdown
    options = []
    opt_pattern = re.findall(r'^\* \*\*([A-F])\.\*\* (.+)$', body, re.MULTILINE)
    for key, text in opt_pattern:
        options.append({"key": key, "text": text.strip()})

    # Determine answer
    answer_list = []
    ans = ans_info.get("answer", {})
    if isinstance(ans, dict):
        if "choice" in ans:
            answer_list = [ans["choice"]]
        elif "choices" in ans:
            answer_list = ans["choices"]
        # For complex answers (dropdowns, drag-drop), store as explanation
    explanation_vi = ans_info.get("explanation", "")

    # Determine type
    if not options:
        qtype = "drag-drop"
    elif len(options) == 2 and options[0]["key"] == "A" and ("Yes" in options[0]["text"] or "No" in options[1]["text"]):
        qtype = "yesno"
    elif len(answer_list) > 1:
        qtype = "multiple"
    else:
        qtype = "single"

    # Build full prompt from body (remove options lines for cleaner display)
    prompt_lines = []
    for line in body.split('\n'):
        if re.match(r'^\* \*\*[A-F]\.\*\*', line):
            continue
        if line.strip() == '---':
            continue
        prompt_lines.append(line)
    prompt = '\n'.join(prompt_lines).strip()
    # Clean up markdown formatting
    prompt = re.sub(r'\*\*(.+?)\*\*', r'\1', prompt)  # Remove bold
    prompt = prompt.replace('```python', '').replace('```bicep', '').replace('```', '')

    # For complex answer types, build explanation with answer details
    if isinstance(ans, dict) and not answer_list:
        # Build answer string from dict
        ans_parts = []
        for k, v in ans.items():
            ans_parts.append(f"{k}: {v}")
        answer_display = "; ".join(ans_parts)
        if explanation_vi:
            explanation_vi = f"Answer: {answer_display}\n\n{explanation_vi}"
        else:
            explanation_vi = f"Answer: {answer_display}"

    sample1.append({
        "id": qnum,
        "label": f"Question {qnum}",
        "topic": "AI-103",
        "type": qtype,
        "prompt": prompt,
        "questionImages": [],
        "options": options,
        "answer": answer_list,
        "explanation": explanation_vi,
        "explanationImages": []
    })

print(f"Sample 1: Built {len(sample1)} questions")

# ============================================================
# SAMPLE 2: questions-data (4)/ folder (35 questions)
# ============================================================
folder = os.path.join(base, "questions-data (4)")
sample2_raw = []
for f in sorted(os.listdir(folder)):
    if f.endswith(".json"):
        with open(os.path.join(folder, f), encoding="utf-8") as fh:
            data = json.load(fh)
            sample2_raw.extend(data)

# Sort by numeric label
def extract_num(q):
    m2 = re.search(r'\d+', q.get("label", "0"))
    return int(m2.group()) if m2 else 0

sample2_raw.sort(key=extract_num)
print(f"Sample 2: {len(sample2_raw)} questions from questions-data folder")

sample2 = []
for q in sample2_raw:
    # Determine type
    if not q["options"]:
        qtype = "drag-drop"
    elif len(q["options"]) == 2 and q["options"][0]["key"] == "A" and ("Yes" in q["options"][0]["text"] or "No" in q["options"][1]["text"]):
        qtype = "yesno"
    else:
        correct = q.get("correctAnswer", "")
        if "," in correct:
            qtype = "multiple"
        else:
            qtype = "single"

    # Parse correct answer
    correct = q.get("correctAnswer", "")
    if correct:
        answer_list = [c.strip() for c in correct.split(",") if c.strip()]
    else:
        answer_list = []

    sample2.append({
        "label": q.get("label", ""),
        "topic": "AI-103",
        "type": qtype,
        "prompt": q["question"],
        "questionImages": q.get("questionImages", []),
        "options": q.get("options", []),
        "answer": answer_list,
        "explanation": q.get("explanation", ""),
        "explanationImages": q.get("explanationImages", [])
    })

# ============================================================
# MERGE: Sample 1 (Q1-65) + Sample 2 (Q66-100)
# ============================================================
all_questions = []

# Add sample 1
for q in sample1:
    all_questions.append(q)

# Add sample 2 with new IDs starting from 66
for i, q in enumerate(sample2, 66):
    q["id"] = i
    q["label"] = q.get("label", f"Question {i}")
    all_questions.append(q)

print(f"\nTotal merged: {len(all_questions)} questions")
img_count = sum(1 for q in all_questions if q.get("questionImages"))
exp_img_count = sum(1 for q in all_questions if q.get("explanationImages"))
print(f"Questions with images: {img_count}")
print(f"Questions with explanation images: {exp_img_count}")

# Build output
output = {
    "metadata": {
        "title": "AI-103 Practice Exam",
        "totalQuestions": len(all_questions),
        "version": "3.0",
        "sources": ["AI-103.md (65 questions)", "questions-data folder (35 questions)"]
    },
    "questions": all_questions
}

# Write questions.json
out_path = os.path.join(base, "questions.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print(f"\nWrote {out_path} with {len(all_questions)} questions")

# Write questions-inline.js
inline_path = os.path.join(base, "questions-inline.js")
with open(inline_path, "w", encoding="utf-8") as f:
    f.write("window._INLINE_QUESTIONS = ")
    json.dump(all_questions, f, ensure_ascii=False)
    f.write(";")
print(f"Wrote {inline_path}")
