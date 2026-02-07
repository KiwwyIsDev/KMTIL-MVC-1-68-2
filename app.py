from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import models

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="exam-secret-key-2569")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = models.authenticate(username, password)
    if user:
        request.session["user"] = user
        return RedirectResponse(url="/promises", status_code=303)
    return templates.TemplateResponse("login.html", {
        "request": request, "error": "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"
    })


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


def get_current_user(request: Request):
    return request.session.get("user")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return RedirectResponse(url="/promises")


@app.get("/promises", response_class=HTMLResponse)
async def all_promises(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login")

    promises = models.get_all_promises()
    politicians = {p["id"]: p for p in models.get_all_politicians()}
    campaigns = {c["id"]: c for c in models.get_all_campaigns()}

    return templates.TemplateResponse("promises_all.html", {
        "request": request,
        "promises": promises,
        "politicians": politicians,
        "campaigns": campaigns,
        "user": user,
    })


@app.get("/promises/{promise_id}", response_class=HTMLResponse)
async def promise_detail(request: Request, promise_id: int):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login")

    promise = models.get_promise(promise_id)
    if not promise:
        raise HTTPException(status_code=404, detail="ไม่พบคำสัญญา")

    politician = models.get_politician(promise["politician_id"])
    campaign = models.get_campaign(promise.get("campaign_id"))
    updates = models.get_updates_by_promise(promise_id)

    return templates.TemplateResponse("promise_detail.html", {
        "request": request,
        "promise": promise,
        "politician": politician,
        "campaign": campaign,
        "updates": updates,
        "user": user,
    })


@app.get("/promises/{promise_id}/update", response_class=HTMLResponse)
async def update_form(request: Request, promise_id: int):
    user = get_current_user(request)
    if not user or user["role"] != "admin":
        return RedirectResponse(url="/login")

    promise = models.get_promise(promise_id)
    if not promise:
        raise HTTPException(status_code=404, detail="ไม่พบคำสัญญา")

    if promise["status"] == "เงียบหาย":
        return RedirectResponse(url=f"/promises/{promise_id}", status_code=303)

    return templates.TemplateResponse("promise_update.html", {
        "request": request,
        "promise": promise,
        "user": user,
    })


@app.post("/promises/{promise_id}/update")
async def submit_update(
    request: Request,
    promise_id: int,
    detail: str = Form(...),
    new_status: str = Form(...)
):
    user = get_current_user(request)
    if not user or user["role"] != "admin":
        return RedirectResponse(url="/login")

    promise = models.get_promise(promise_id)
    if not promise or promise["status"] == "เงียบหาย":
        return RedirectResponse(url=f"/promises/{promise_id}", status_code=303)

    models.add_promise_update(promise_id, detail)

    if new_status in ["ยังไม่เริ่ม", "กำลังดำเนินการ", "เงียบหาย"]:
        models.update_promise_status(promise_id, new_status)

    return RedirectResponse(url=f"/promises/{promise_id}", status_code=303)


@app.get("/politicians", response_class=HTMLResponse)
async def all_politicians(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login")

    politicians = models.get_all_politicians()
    return templates.TemplateResponse("politicians.html", {
        "request": request,
        "politicians": politicians,
        "user": user,
    })


@app.get("/politicians/{politician_id}", response_class=HTMLResponse)
async def politician_detail(request: Request, politician_id: str):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login")

    politician = models.get_politician(politician_id)
    if not politician:
        raise HTTPException(status_code=404, detail="ไม่พบนักการเมือง")

    promises = models.get_promises_by_politician(politician_id)

    return templates.TemplateResponse("politician_detail.html", {
        "request": request,
        "politician": politician,
        "promises": promises,
        "user": user,
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
