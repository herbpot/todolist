# todolist

Tkinter 기반의 할 일 관리 데스크톱 애플리케이션입니다.

## 개요

todolist는 Python의 Tkinter를 사용하여 만든 간단하면서도 실용적인 TODO 리스트 관리 프로그램입니다. 할 일을 추가하고, 완료 표시하며, 걸린 시간을 자동으로 추적합니다. 모든 데이터는 텍스트 파일로 저장되어 프로그램을 재시작해도 유지됩니다.

## 주요 기능

- **할 일 추가**: 새로운 TODO 항목 생성
- **완료 표시**: 완료한 항목 체크 및 소요 시간 자동 계산
- **항목 삭제**: 불필요한 항목 제거
- **시간 추적**: 생성부터 완료까지 걸린 시간 자동 기록
- **데이터 영속성**: todolist.txt 파일로 자동 저장
- **간단한 GUI**: 직관적인 Tkinter 인터페이스

## 기술 스택

- **Python 3.x**
- **Tkinter** - GUI 프레임워크
- **datetime** - 시간 계산
- **time** - 타임스탬프

## 프로젝트 구조

```
todolist/
├── app.py              # 메인 애플리케이션
└── todolist.txt        # 데이터 저장 파일 (자동 생성)
```

## 설치 및 실행

### 사전 요구사항

- Python 3.x (Tkinter 포함)

### 1. 저장소 클론

```bash
git clone https://github.com/herbpot/todolist.git
cd todolist
```

### 2. 실행

```bash
python app.py
```

## 사용 방법

### 기본 사용

1. **할 일 추가**
   - 입력 필드에 할 일 입력
   - "생성" 버튼 클릭

2. **할 일 완료**
   - 리스트에서 항목 선택
   - "끝" 버튼 클릭
   - 소요 시간이 자동으로 계산되어 표시됨

3. **할 일 삭제**
   - 리스트에서 항목 선택
   - "삭제" 버튼 클릭
   - 확인 대화상자에서 "예" 선택

### 화면 구성

```
┌─────────────────────────────────┐
│ [아이디 | 할 일 | 끝 | 걸린시간] │ ← 헤더
├─────────────────────────────────┤
│                                 │
│  0| 프로젝트 제출 | no | ...    │
│  1| 책 읽기 | yes | 2:15:30     │
│  2| 운동하기 | no | ...         │
│                                 │ ← 리스트박스
├─────────────────────────────────┤
│ 새 할일                         │
│ [____________입력 필드__________]│
│                                 │
│   [생성]   [끝]     [삭제]      │ ← 버튼
└─────────────────────────────────┘
```

## 데이터 구조

### 내부 데이터 구조

```python
todolist = {
    0: ["프로젝트 제출", "no", "1644652800.0"],
    1: ["책 읽기", "yes", "2:15:30"],
    2: ["운동하기", "no", "1644656400.0"]
}
```

| 필드 | 설명 |
|------|------|
| 아이디 | 할 일의 고유 번호 |
| 할 일 | 할 일 내용 |
| 완료 여부 | "yes" 또는 "no" |
| 시간 | 미완료: 생성 시각(Unix timestamp) / 완료: 소요 시간(HH:MM:SS) |

### todolist.txt 파일 형식

```
0|프로젝트제출|no|1644652800.0
1|책읽기|yes|2:15:30
2|운동하기|no|1644656400.0
```

## 핵심 기능 구현

### 1. 할 일 추가

```python
def addnewtodo(todo):
    newtodo = [todo, "no", time()]
    todolist[len(todolist)] = newtodo
    listbox.insert(END, newtodo)
    printtodo()
```

- 현재 시각(timestamp)을 저장하여 나중에 소요 시간 계산

### 2. 완료 처리 및 시간 계산

```python
def donetodo(num : int):
    i = todolist[keys[num-1]]
    i[1] = 'yes'
    res = datetime.timedelta(seconds=(time() - float(i[2])))
    i[2] = str(res).split('.')[0]
    printtodo()
```

- 현재 시각에서 생성 시각을 빼서 소요 시간 계산
- `timedelta`로 "H:MM:SS" 형식으로 변환

### 3. 파일 저장 및 로드

```python
def printtodo():
    with open(os.path.dirname(os.path.abspath(__file__))+'/todolist.txt','w') as f:
        for i in todolist.keys():
            printer = str(i) + '| '
            for j in todolist[i]:
                printer += str(j) + ' | '
            f.write(printer.replace(' ',''))

def load():
    with open(os.path.dirname(os.path.abspath(__file__))+'/todolist.txt','r') as f :
        for i in f.readlines() :
            i = i.split("|")
            # ... 파싱 로직
```

### 4. GUI 이벤트 핸들링

```python
def btn_add(event):
    subject = entry.get().strip()
    if not subject:
        showerror("오류", "내용을 입력해 주세요")
        return
    addnewtodo(subject)

b1.bind('<Button-1>', btn_add)
b2.bind('<Button-1>', btn_done)
b3.bind('<Button-1>', btn_remove)
```

## 사용 예시

### 시나리오 1: 간단한 할 일 관리

```
1. "알고리즘 문제 풀기" 입력 → 생성 클릭
   → 0| 알고리즘 문제 풀기 | no | 1644652800.0

2. 1시간 후 문제를 다 품
   → 항목 선택 후 "끝" 클릭
   → 0| 알고리즘 문제 풀기 | yes | 1:00:00

3. 불필요한 항목 삭제
   → 항목 선택 후 "삭제" 클릭
```

### 시나리오 2: 장기 프로젝트 추적

```
1. "졸업 프로젝트" 추가 (2월 1일)
2. 3월 15일에 완료 표시
   → 걸린시간: 1008:00:00 (42일)
```

## 에러 처리

### 빈 입력 방지

```python
if not subject:
    showerror("오류", "내용을 입력해 주세요")
    return
```

### 선택 없이 버튼 클릭 방지

```python
sel = listbox.curselection()
if not sel:
    showerror("오류", "리스트를 먼저 선택해 주세요")
    return
```

### 삭제 확인 대화상자

```python
if askyesno("확인", "정말로 삭제하시겠습니까?"):
    id = sel[0]
    todolist.pop(id)
```

## 단축키

현재 마우스 클릭만 지원하지만, 다음 단축키를 추가할 수 있습니다:

```python
# 개선안
root.bind('<Return>', btn_add)      # Enter: 추가
root.bind('<Delete>', btn_remove)   # Delete: 삭제
root.bind('<Control-d>', btn_done)  # Ctrl+D: 완료
```

## 향후 개선 방향

- [ ] 우선순위 설정 기능
- [ ] 마감일 설정 및 알림
- [ ] 카테고리/태그 분류
- [ ] 검색 기능
- [ ] 통계 대시보드 (완료율, 평균 소요 시간)
- [ ] 다크 모드 지원
- [ ] 내보내기/가져오기 (JSON, CSV)
- [ ] 데이터베이스 연동 (SQLite)
- [ ] 멀티 리스트 (개인/업무 분리)
- [ ] 드래그 앤 드롭으로 순서 변경

## 성능 및 안정성 개선

### 1. ID 관리 개선

현재는 `len(todolist)`를 ID로 사용하여 삭제 후 문제 발생 가능:

```python
# 개선안
def get_next_id():
    if not todolist:
        return 0
    return max(todolist.keys()) + 1
```

### 2. 파일 백업

```python
import shutil
from datetime import datetime

def backup_todolist():
    backup_name = f"todolist_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    shutil.copy('todolist.txt', backup_name)
```

### 3. 예외 처리 강화

```python
try:
    load()
except FileNotFoundError:
    print("새로운 TODO 리스트를 시작합니다.")
except Exception as e:
    showerror("오류", f"파일 로드 실패: {e}")
```

## 트러블슈팅

### 창이 항상 위에 표시되지 않음

```python
# app.py:113
root.attributes("-topmost", True)
```

이 줄이 `root.mainloop()` 이후에 있어 실행되지 않습니다. 수정:

```python
def main():
    load()
    root.attributes("-topmost", True)  # 이 줄을 위로 이동
    b1.bind('<Button-1>', btn_add)
    b2.bind('<Button-1>',btn_done)
    b3.bind('<Button-1>', btn_remove)
    root.mainloop()
```

### todolist.txt 파일이 생성되지 않음

첫 실행 시 파일이 없으면 오류가 발생할 수 있습니다. 수정:

```python
def load():
    if not os.path.exists('todolist.txt'):
        return
    # ... 나머지 로드 로직
```

## 코드 개선 제안

### 1. 클래스 기반으로 리팩토링

```python
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.todolist = {}
        self.setup_ui()
        self.load()

    def setup_ui(self):
        # UI 초기화
        pass

    def add_todo(self, text):
        # ...
        pass
```

### 2. JSON 형식으로 데이터 저장

```python
import json

def save():
    with open('todolist.json', 'w', encoding='utf-8') as f:
        json.dump(todolist, f, indent=2, ensure_ascii=False)
```

### 3. 설정 파일 분리

```python
# config.py
WINDOW_SIZE = "300x500"
ALWAYS_ON_TOP = True
AUTO_SAVE_INTERVAL = 60  # 초
```

## 참고 자료

- [Tkinter 문서](https://docs.python.org/3/library/tkinter.html)
- [datetime 모듈](https://docs.python.org/3/library/datetime.html)
- [Tkinter Tutorial](https://realpython.com/python-gui-tkinter/)

## 라이선스

교육 목적으로 작성된 프로젝트입니다.
