# ไฟล์ใดทําหน้าที่อะไรใน MVC และทํางานร่วมกันอย่างไร 

## models.py
Model จัดการข้อมูลทั้งหมด อ่าน/เขียน JSON ไฟล์ มีฟังก์ชันสำหรับดึงข้อมูลนักการเมือง คำสัญญา ความคืบหน้า และ authenticate ผู้ใช้

## templates/
View เป็น Jinja2 HTML templates แยกแต่ละหน้าจอ มี base.html เป็น layout หลัก

## app.py
Controller เป็นตัว route request ไปยัง Model แล้วส่งข้อมูลไป render ที่ View
การทำงานร่วมกัน ผู้ใช้เข้า URL ส่งไปหา app.py (Controller) 
เมื่อรับ request ทำการเรียก models.py (Model) fetchหรือบันทึกข้อมูลและส่งข้อมูลไป render ที่ templates (View)ทำการส่ง html กลับผู้ใช้

# สรุป Routes/Actions หลัก และหน้าจอ View สําคัญ

| Route | Method | หน้าที่ |
|-------|--------|---------|
| /login | GET/POST | หน้า login |
| /logout | GET | ออกจากระบบ |
| /promises | GET | แสดงคำสัญญาทั้งหมด เรียงตามวันที่ |
| /promises/{id} | GET | รายละเอียดคำสัญญาและรายการประวัติที่ถูกอัปเดต |
| /promises/{id}/update | GET/POST | ฟอร์มเพิ่มความคืบหน้า (admin) |
| /politicians | GET | รายชื่อนักการเมืองทั้งหมด |
| /politicians/{id} | GET | คำสัญญาของนักการเมืองแต่ละคน |

## view page
- login.html หน้า login
- promises_all.html หน้ารวมคำสัญญาทั้งหมด
- promise_detail.html หน้ารายละเอียดคำสัญญาและรายการประวัติที่ถูกอัปเดต
- promise_update.html หน้าฟอร์มอัปเดตความคืบหน้า
- politicians.html หน้ารายชื่อนักการเมืองทั้งหมด
- politician_detail.html หน้าแสดงคำสัญญาของนักการเมืองแต่ละคน