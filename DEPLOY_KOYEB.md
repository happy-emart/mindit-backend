# Koyeb 배포 가이드

## 1. GitHub에 코드 올리기

프로젝트가 아직 GitHub에 없다면:

```bash
cd /Users/yddook/ukgrade/prog/mindit/mindit-backend
git init
git add main.py services.py requirements.txt Dockerfile .dockerignore
git commit -m "Add Koyeb deploy"
git remote add origin https://github.com/<YOUR_USERNAME>/<REPO_NAME>.git
git branch -M main
git push -u origin main
```

`.env`는 반드시 제외 (이미 .dockerignore에 있음). Koyeb에서 환경변수로 넣을 예정.

---

## 2. Koyeb에서 서비스 만들기

1. [Koyeb 콘솔](https://app.koyeb.com/) 로그인
2. **Create Web Service** 클릭
3. **GitHub** 선택 → 저장소·브랜치 선택 (또는 Public repo URL 입력)
4. **Build** 설정
   - Builder: **Dockerfile** 선택 (Dockerfile 사용 시)
   - 또는 Builder: **Buildpack** 선택 후 **Run command** Override:
     ```bash
     uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
     ```
5. **Environment variables** 에 아래 추가 (이름/값은 본인 값으로)
   - `SUPABASE_URL` = (Supabase 프로젝트 URL)
   - `SUPABASE_KEY` = (Supabase anon key)
   - `GOOGLE_API_KEY` = (Google AI API 키)
6. **Deploy** 클릭

---

## 3. 배포 후

- 서비스 URL: `https://<서비스이름>-<앱이름>.koyeb.app`
- 헬스 체크: `GET /` → `{"message":"Mindit Server is Running! 🚀"}`
- API 문서: `https://<URL>/docs`

---

## 4. 참고

- Koyeb이 `PORT` 환경변수를 주입하므로, Dockerfile/Run command는 그 포트를 사용하도록 되어 있음.
- 시크릿은 Koyeb 대시보드에서만 설정하고, 코드/이미지에는 넣지 말 것.
