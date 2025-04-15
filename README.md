# HTML to PDF 변환기

HTML 문서를 고품질 PDF 파일로 변환하는 Python 기반 CLI 도구입니다. Playwright를 활용하여 HTML 파일을 PDF로 정확하게 변환하며, 한글 폰트와 특수 문자를 완벽하게 지원합니다.

## 주요 기능

- HTML 파일을 고품질 PDF로 변환
- 한글 폰트 및 특수 문자 지원
- 단일 파일 또는 디렉토리 일괄 변환 지원
- HTML 문자열을 직접 PDF로 변환 가능
- 자동 스타일링과 레이아웃 최적화

## 설치 방법

### 1. 저장소 클론

```bash
git clone https://github.com/yourusername/html-to-pdf.git
cd html-to-pdf
```

### 2. 가상 환경 설정 (Python 3.13 이상 필요)

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 또는 
.venv\Scripts\activate  # Windows
```

### 3. 의존성 설치

```bash
pip install -e .
```

### 4. Playwright 설치

```bash
playwright install
```

## 사용 방법

### 단일 HTML 파일 변환

```bash
python main.py --html path/to/your/file.html
```

출력 경로를 지정하려면:

```bash
python main.py --html path/to/your/file.html --out path/to/output.pdf
```

### 디렉토리 일괄 변환

HTML 디렉토리의 모든 HTML 파일을 PDF로 변환:

```bash
python main.py --batch
```

특정 HTML 디렉토리와 PDF 출력 디렉토리 지정:

```bash
python main.py --batch --html-dir /path/to/html/files --pdf-dir /path/to/output/pdf
```

## 코드에서 직접 사용

```python
import asyncio
from main import convert_html_file, batch_convert_html_files, convert_html_string

# 단일 HTML 파일 변환
asyncio.run(convert_html_file('path/to/your/file.html', 'path/to/output.pdf'))

# 디렉토리 일괄 변환
asyncio.run(batch_convert_html_files('html_directory', 'pdf_directory'))

# HTML 문자열을 직접 PDF로 변환
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>샘플 문서</title>
</head>
<body>
    <h1>안녕하세요!</h1>
    <p>이것은 테스트 HTML 문서입니다.</p>
</body>
</html>
"""
asyncio.run(convert_html_string(html_content, 'output.pdf'))
```

## 디렉토리 구조

```
html-to-pdf/
├── main.py             # 메인 스크립트
├── html/               # HTML 입력 파일 기본 디렉토리
│   ├── chatgpt_guide_book.html
│   ├── claude_guide_book.html
│   └── mcp_guide_book.html
├── pdf/                # PDF 출력 파일 기본 디렉토리
├── pyproject.toml      # 프로젝트 설정
└── README.md           # 이 파일
```

## 주요 기능 설명

### 한글 지원
CSS 스타일을 통해 다양한 한글 폰트를 지원합니다:
- Pretendard
- Apple SD Gothic Neo
- AppleGothic
- Malgun Gothic
- NanumGothic
- Noto Sans KR

### PDF 레이아웃
PDF 출력물은 다음과 같은 설정으로 최적화됩니다:
- A4 용지 크기
- 적절한 여백 설정
- 가독성 높은 폰트 크기 및 줄 간격
- 특수 문자 처리 최적화

### 특수 처리
이 프로그램은 다음과 같은 특수 케이스를 처리합니다:
- 특수 문자(+, © 등) 처리
- 저작권 정보 자동 포맷팅
- 페이지 레이아웃 최적화

## 요구사항

- Python 3.13 이상
- Playwright
- 인터넷 연결 (폰트 다운로드용)

## 라이선스

MIT License

## 기여

1. 이 저장소를 포크하세요
2. 새 기능 브랜치를 만드세요 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋하세요 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 푸시하세요 (`git push origin feature/amazing-feature`)
5. Pull Request를 제출하세요

## 문의

프로젝트에 대한 질문이나 문제가 있으면 이슈를 생성해주세요.