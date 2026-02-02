# Simple Server Premium

로컬 폴더를 웹 서버로 즉시 호스팅하고, 정적 웹사이트 및 Next.js 프로젝트를 배포할 수 있는 현대적인 파이썬 GUI 애플리케이션입니다.

## 주요 기능
- **프리미엄 UI/UX**: 다크 모드 기반의 세련된 카드 레이아웃과 직관적인 인터페이스.
- **다양한 호스팅 모드**:
  - `파일 공유`: 일반적인 디렉토리 브라우징 및 파일 다운로드.
  - `정적 사이트`: `index.html` 기반의 정적 웹사이트 전용 호스팅.
  - `스마트 호스팅`: 웹 기반 프로젝트와 일반 파일을 지능적으로 구분하여 렌더링.
- **Next.js 완벽 지원**: Clean URLs 지원을 통해 빌드된 Next.js(out 폴더) 프로젝트를 완독하게 호스팅.
- **실시간 로깅**: 접속 IP, 요청 경로, 시스템 상태를 실시간으로 모니터링.
- **네트워크 접근 제어**: 내 PC, 로컬 네트워크(LAN), 외부 인터넷(UPnP 지원) 범위 선택 가능.
- **자동 배포 파이프라인**: GitHub Actions를 통한 OS별 실행 파일 빌드 및 도커 이미지 자동 배포.

## 제작자 정보
- **Copyright**: 2008-2026 Rheehose (Rhee Creative)

## 라이선스
이 프로젝트는 **Apache License 2.0** 라이선스에 따라 배포됩니다. 자세한 내용은 `LICENSE` 파일을 확인하세요.

## 면책 사항
**사용에 따른 책임은 사용자 본인에게 있습니다.**
서버를 외부 네트워크에 노출하는 것은 보안 위험을 수반합니다. 공인 IP를 통해 접속을 허용할 경우 반드시 신뢰할 수 있는 네트워크 환경에서 사용하십시오.

## 설치 및 실행
1. 의존성 설치:
   ```bash
   pip install -r requirements.txt
   ```
2. 프로그램 실행:
   ```bash
   python main.py
   # 또는
   ./run.sh
   ```

## 배포 및 빌드
### GitHub Actions (CI/CD)
이 프로젝트는 GitHub에 푸시될 때마다 다음 작업을 자동으로 수행합니다:
1. **버전 태깅**: 패치 버전을 자동으로 올리고 태그를 생성합니다.
2. **바이너리 빌드**: Windows, MacOS, Linux용 단일 실행 파일을 생성하여 릴리즈에 업로드합니다.
3. **도커 배포**: 최신 이미지를 GitHub Container Registry(GHCR)에 푸시합니다.

### 도커 실행 (Headless)
컨테이너 환경에서 서버 엔진만 실행할 수 있습니다:
```bash
docker pull ghcr.io/<your-username>/simple_server:latest
docker run -p 8080:8080 -v /path/to/share:/app/data ghcr.io/<your-username>/simple_server:latest
```
