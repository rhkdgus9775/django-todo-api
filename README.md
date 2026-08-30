# Django Todo API (DRF + JWT)

JWT 인증을 기반으로 한 Todo REST API 프로젝트입니다.

Django REST Framework를 사용하여 사용자별 Todo 관리 기능을 구현했으며,
검색(Search), 정렬(Ordering), 필터링(Filtering), 페이지네이션(Pagination),
Swagger API 문서화까지 적용했습니다.

---

## 기술 스택

- Python 3.14
- Django
- Django REST Framework (DRF)
- SimpleJWT
- SQLite
- django-filter
- drf-spectacular (Swagger)

---

## 주요 기능

### 사용자 인증

- 회원가입
- JWT 로그인
- Access Token / Refresh Token 인증

### Todo 관리

- Todo 생성(Create)
- Todo 목록 조회(List)
- Todo 상세 조회(Retrieve)
- Todo 수정(Update)
- Todo 삭제(Delete)

### 추가 기능

- 사용자별 Todo 조회
- 검색(Search)
- 정렬(Ordering)
- 완료 여부 필터링(Filtering)
- 페이지네이션(Pagination)

### API 문서

Swagger(OpenAPI)를 이용한 API 문서 제공

```
/api/docs/
```

---

## 프로젝트 구조

```
django_study/
│
├── api/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│
├── manage.py
├── README.md
└── requirements.txt

```

---

## API 목록

| Method | URL | 설명 |
|--------|-----|------|
| POST | /api/register/ | 회원가입 |
| POST | /api/token/ | 로그인(JWT 발급) |
| POST | /api/token/refresh/ | Access Token 재발급 |
| GET | /api/todos/ | Todo 목록 조회 |
| POST | /api/todos/ | Todo 생성 |
| GET | /api/todos/{id}/ | Todo 상세 조회 |
| PATCH | /api/todos/{id}/ | Todo 수정 |
| DELETE | /api/todos/{id}/ | Todo 삭제 |

---

## 검색

```
GET /api/todos/?search=공부
```

---

## 정렬

```
GET /api/todos/?ordering=created_at
```

```
GET /api/todos/?ordering=-created_at
```

---

## 완료 여부 필터링

```
GET /api/todos/?completed=true
```

```
GET /api/todos/?completed=false
```

---

## 페이지네이션

```
GET /api/todos/?page=2
```

---

## 실행 방법

### 1. 저장소 복제

```bash
git clone <저장소 주소>
cd django-todo-api
```

### 2. 가상환경 생성 및 실행

Windows PowerShell 기준:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 환경변수 설정

프로젝트 루트에 `.env` 파일을 만들고 다음 내용을 입력합니다.

```env
DJANGO_SECRET_KEY=새로 생성한 Django Secret Key
```

Secret Key 생성 명령:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. 데이터베이스 생성

```bash
python manage.py migrate
```

### 6. 개발 서버 실행

```bash
python manage.py runserver
```

### 7. Swagger API 문서 접속

```text
http://127.0.0.1:8000/api/docs/
```

---

## 인증 사용 흐름

1. `/api/register/`에서 회원가입
2. `/api/token/`에서 Access Token과 Refresh Token 발급
3. 요청 헤더에 Access Token 추가

```text
Authorization: Bearer <access_token>
```

4. Access Token이 만료되면 `/api/token/refresh/`에서 재발급

---

## 주요 구현 내용

### 사용자별 데이터 분리

로그인한 사용자의 Todo만 조회하도록 QuerySet을 제한했습니다.

```python
def get_queryset(self):
    return Todo.objects.filter(user=self.request.user)
```

Todo 생성 시 요청한 사용자를 자동으로 저장합니다.

```python
def perform_create(self, serializer):
    serializer.save(user=self.request.user)
```

이 구조를 통해 다른 사용자의 Todo를 조회하거나 수정·삭제할 수 없도록 했습니다.

### 비밀번호 보안

회원가입 시 Django의 `create_user()`를 사용해 비밀번호가 평문으로 저장되지 않고 해시 처리되도록 구현했습니다.

### 환경변수 분리

Django `SECRET_KEY`를 코드에 직접 작성하지 않고 `.env` 파일로 분리했습니다. `.env`는 `.gitignore`에서 제외해 공개 저장소에 포함되지 않도록 했습니다.

---

## 개선 가능 사항

- PostgreSQL 적용
- Docker 기반 실행 환경 구성
- 배포 환경 구축
- 비밀번호 정책 및 회원 정보 기능 확장

---

## 프로젝트를 통해 배운 점

- Django REST Framework를 이용한 REST API 설계
- JWT 기반 인증(Authentication)
- Serializer를 이용한 데이터 검증
- Generic View 활용
- 사용자별 데이터 접근 제어
- Search / Ordering / Filtering 구현
- Pagination 적용
- Swagger(OpenAPI)를 이용한 API 문서화

## 앞으로 개선하고 싶은 점
- pytest를 이용한 테스트 코드 작성
- Docker를 이용한 컨테이너 환경 구성
- PostgreSQL 적용
- AWS 배포
- GitHub Actions를 이용한 CI/CD 구축