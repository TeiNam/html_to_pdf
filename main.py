import asyncio
import os
from argparse import ArgumentParser
import glob
from pathlib import Path

from playwright.async_api import async_playwright


async def convert_html_file(html_path, pdf_path=None):
    """HTML 파일을 PDF로 변환합니다."""
    # PDF 경로가 지정되지 않은 경우 기본 경로 설정
    if pdf_path is None:
        # HTML 파일 경로에서 파일명만 추출
        html_filename = os.path.basename(html_path)
        html_name = os.path.splitext(html_filename)[0]

        # root/pdf 폴더에 동일한 이름으로 PDF 저장
        pdf_dir = os.path.join(os.path.dirname(os.path.dirname(html_path)), "pdf")
        os.makedirs(pdf_dir, exist_ok=True)  # pdf 디렉토리 생성
        pdf_path = os.path.join(pdf_dir, f"{html_name}.pdf")

    print(f"{html_path} 파일을 {pdf_path}로 변환합니다...")

    try:
        # HTML 파일 읽기
        with open(html_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # HTML 문자열 처리 로직
        if not html_path.endswith('.html') and not html_path.startswith('http'):
            # HTML 문자열에 폰트 클래스 추가
            html_content = html_content.replace('+', '<span class="special-chars">+</span>')
            html_content = html_content.replace('©', '<span class="special-chars">©</span>')

            # 저작권 정보 처리 (맺음말에 연결)
            if '© 2025' in html_content:
                replacements = [
                    ('맺음말: AI 시대를 항해하는 여러분을 위한 안내',
                     '<div class="final-content">맺음말: AI 시대를 항해하는 여러분을 위한 안내'),
                    ('여러분의 성공적인 AI 여정을 기원하며,',
                     '여러분의 성공적인 AI 여정을 기원하며,</div>'),
                    ('© 2025 [TeiNam',
                     '<div id="copyright">© 2025 [TeiNam'),
                    ('본 전자책의 내용 및 코드는 학습 목적으로 제공됩니다.',
                     '본 전자책의 내용 및 코드는 학습 목적으로 제공됩니다.</div>')
                ]

                for old_text, new_text in replacements:
                    if old_text in html_content:
                        html_content = html_content.replace(old_text, new_text)

        # CSS 스타일 추가
        css_string = '''
        @page {
            size: A4;
            margin: 1.5cm 1.2cm; /* 페이지 여백 */
        }

        /* 폰트 설정 - macOS 한글 폰트 명시적 포함 */
        @font-face {
            font-family: 'Pretendard';
            src: url('fonts/PretendardVariable.woff2') format('woff2');
            font-weight: normal;
            font-style: normal;
        }

        /* macOS 기본 한글 폰트 지정 */
        @font-face {
            font-family: 'AppleSDGothicNeo';
            src: local('Apple SD Gothic Neo');
            font-weight: normal;
            font-style: normal;
            unicode-range: U+0000-FFFF; /* 전체 유니코드 범위 지원 */
        }

        @font-face {
            font-family: 'AppleGothic';
            src: local('AppleGothic');
            font-weight: normal;
            font-style: normal;
            unicode-range: U+0000-FFFF;
        }

        body {
            /* 확장된 폰트 fallback 순서 - 특수 문자 지원 강화 */
            font-family: 'Pretendard', 'AppleSDGothicNeo', 'Apple SD Gothic Neo', 'AppleGothic', 
                         'Malgun Gothic', 'NanumGothic', 'Noto Sans KR', 'Noto Sans CJK KR', 
                         sans-serif;
            line-height: 1.5;
            font-size: 10pt;
            color: #333;
            word-wrap: break-word;
            overflow-wrap: break-word;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        /* 특수 문자용 폰트 명시적 지정 */
        .special-char {
            font-family: 'Arial', 'Helvetica', sans-serif;
        }

        /* 기존 CSS 내용 */
        p {
            margin-top: 0;
            margin-bottom: 0.8em;
        }
        h1, h2, h3, h4 {
            font-weight: 700;
            line-height: 1.3;
        }
        h1 { font-size: 2em; margin-bottom: 1em; }
        h2.chapter-title {
            font-size: 1.6em;
            margin-top: 0;
            margin-bottom: 1em;
            padding-top: 0.5cm;
            border-bottom: 2px solid #10a37f;
            color: #10a37f;
            page-break-after: avoid;
        }
        /* 나머지 CSS 스타일 유지 */
        '''

        # 전체 HTML 문서 생성
        full_html = f"""<!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>{css_string}</style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        # 임시 HTML 파일 저장
        temp_html_path = f"{os.path.splitext(html_path)[0]}_temp.html"
        with open(temp_html_path, 'w', encoding='utf-8') as f:
            f.write(full_html)

        # Playwright 실행
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # 로컬 파일 로드
            await page.goto(f"file://{os.path.abspath(temp_html_path)}")

            # PDF 직접 저장 (수정된 부분)
            await page.pdf(
                path=pdf_path,
                format="A4",
                margin={
                    "top": "1.5cm",
                    "right": "1.2cm",
                    "bottom": "1.5cm",
                    "left": "1.2cm"
                },
                print_background=True,
                prefer_css_page_size=True
            )

            await browser.close()

            # 임시 파일 삭제
            if os.path.exists(temp_html_path):
                os.remove(temp_html_path)

            print(f"PDF 생성 완료: {pdf_path}")
            return pdf_path

    except FileNotFoundError:
        print(f"오류: {html_path} 파일을 찾을 수 없습니다.")
        raise
    except Exception as e:
        print(f"변환 중 오류 발생: {str(e)}")
        raise


async def batch_convert_html_files(html_dir, pdf_dir=None):
    """특정 디렉토리의 모든 HTML 파일을 PDF로 일괄 변환"""
    # HTML 디렉토리 확인
    if not os.path.exists(html_dir):
        print(f"오류: {html_dir} 디렉토리가 존재하지 않습니다.")
        return

    # PDF 디렉토리 설정
    if pdf_dir is None:
        # root/pdf 폴더로 설정
        root_dir = os.path.dirname(html_dir)
        pdf_dir = os.path.join(root_dir, "pdf")

    # PDF 디렉토리 생성
    os.makedirs(pdf_dir, exist_ok=True)

    # HTML 파일 목록 가져오기
    html_files = glob.glob(os.path.join(html_dir, "*.html"))

    if not html_files:
        print(f"{html_dir} 디렉토리에 HTML 파일이 없습니다.")
        return

    print(f"총 {len(html_files)}개의 HTML 파일을 변환합니다...")

    # 각 HTML 파일을 PDF로 변환
    tasks = []
    for html_path in html_files:
        html_filename = os.path.basename(html_path)
        html_name = os.path.splitext(html_filename)[0]
        pdf_path = os.path.join(pdf_dir, f"{html_name}.pdf")

        # 비동기 작업 추가
        tasks.append(convert_html_file(html_path, pdf_path))

    # 모든 변환 작업 실행
    await asyncio.gather(*tasks)

    print(f"모든 HTML 파일 변환이 완료되었습니다. 결과물은 {pdf_dir}에 저장되었습니다.")


async def convert_html_string(html_string, pdf_output_path):
    """HTML 문자열을 PDF로 변환하는 편의 함수"""
    # 임시 HTML 파일 생성
    temp_dir = os.path.dirname(pdf_output_path)
    if not temp_dir:
        temp_dir = "."
    temp_html_path = os.path.join(temp_dir, 'temp_content.html')

    # CSS 스타일 추가
    css_string = '''
    @page {
        size: A4;
        margin: 1.5cm 1.2cm;
    }
    body {
        font-family: 'Pretendard', 'AppleSDGothicNeo', sans-serif;
        line-height: 1.5;
        font-size: 10pt;
        color: #333;
    }
    /* 나머지 필요한 CSS 스타일 */
    '''

    full_html = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>{css_string}</style>
    </head>
    <body>
        {html_string}
    </body>
    </html>
    """

    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    try:
        # Playwright 실행
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # 로컬 파일 로드
            await page.goto(f"file://{os.path.abspath(temp_html_path)}")

            # PDF 직접 저장 (수정된 부분)
            await page.pdf(
                path=pdf_output_path,
                format="A4",
                margin={
                    "top": "1.5cm",
                    "right": "1.2cm",
                    "bottom": "1.5cm",
                    "left": "1.2cm"
                },
                print_background=True,
                prefer_css_page_size=True
            )

            await browser.close()

            print(f"PDF 생성 완료: {pdf_output_path}")
            return pdf_output_path

    finally:
        # 임시 파일 정리
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)


if __name__ == "__main__":
    parser = ArgumentParser(description='HTML을 PDF로 변환합니다.')
    parser.add_argument('--html', help='Input HTML file path or URL')
    parser.add_argument('--out', help='Output PDF file path')
    parser.add_argument('--batch', action='store_true', help='모든 HTML 파일 일괄 변환')
    parser.add_argument('--html-dir', default='html', help='HTML 파일이 있는 디렉토리 (기본값: html)')
    parser.add_argument('--pdf-dir', default=None, help='PDF 파일을 저장할 디렉토리 (기본값: root/pdf)')

    args = parser.parse_args()

    # 프로젝트 루트 디렉토리 설정 (실행 파일의 디렉토리)
    root_dir = os.path.dirname(os.path.abspath(__file__))

    if args.batch:
        # 일괄 변환 모드
        html_dir = args.html_dir
        if not os.path.isabs(html_dir):
            html_dir = os.path.join(root_dir, html_dir)

        pdf_dir = args.pdf_dir
        if pdf_dir is not None and not os.path.isabs(pdf_dir):
            pdf_dir = os.path.join(root_dir, pdf_dir)
        else:
            pdf_dir = os.path.join(root_dir, "pdf")

        # 일괄 변환 실행
        asyncio.run(batch_convert_html_files(html_dir, pdf_dir))

    elif args.html:
        # 단일 파일 변환 모드
        html_path = args.html
        if not os.path.isabs(html_path):
            if os.path.exists(html_path):
                html_path = os.path.abspath(html_path)
            else:
                # root/html 폴더에서 검색
                html_path = os.path.join(root_dir, "html", html_path)

        # PDF 경로 설정
        pdf_path = args.out
        if pdf_path is None:
            # 기본 PDF 경로 설정 (convert_html_file 함수가 처리)
            pass
        elif not os.path.isabs(pdf_path):
            # 상대 경로일 경우 root/pdf 폴더 기준으로 설정
            pdf_dir = os.path.join(root_dir, "pdf")
            os.makedirs(pdf_dir, exist_ok=True)
            pdf_path = os.path.join(pdf_dir, pdf_path)

        # 파일 변환 실행
        asyncio.run(convert_html_file(html_path, pdf_path))

    else:
        print("오류: --html 파일 경로나 --batch 옵션을 지정해야 합니다.")
        parser.print_help()