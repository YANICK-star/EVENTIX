# 🎟️ EVENTIX — Cameroon Smart Events Management Platform

> **Academic Project Context:** Bachelor 3 Software Engineering  
> **Institution:** IAI Cameroon / CET Paul Biya  
> **Core Framework:** Django 6.x (Python) with MVT Architecture  
> **Target Deployment:** Cameroon Event Ecosystem (Yaoundé, Douala, Bafoussam, Bamenda, Buea, Garoua)

---

## 🌟 Overview & Problem Statement

In Cameroon, organizing events across universities, cultural festivals, sports arenas, and private family milestones has long suffered from:
1. **Capacity Mismanagement & Overcrowding:** Lack of real-time seat tracking causing severe overbooking.
2. **Ticketing Fraud & Gate-Crashing:** Easily duplicated paper tickets and counterfeit Mobile Money screenshots.
3. **Entrance Bottlenecks:** Long queues caused by ushers manually checking clipboard guest lists under adverse weather conditions.
4. **Post-Event Reconciliation Inefficiencies:** Manual cash tracking causing financial and headcount discrepancies.

**Eventix** solves these four bottlenecks through an enterprise-grade Django MVT platform with **atomic capacity locking**, **cryptographic QR boarding passes**, and **instant camera-based door check-in**.

---

## 🎨 Dual Theme & Bilingual Experience

- **Fresh Light Theme by Default:** Clean and modern interface matching the official logo, designed for bright daylight and university environments.
- **Theme Selection Button:** One-click toggle (☀️ / 🌙) in the top navigation bar to switch between Light Mode and Dark Mode, seamlessly persisted via `localStorage`.
- **Bilingual Interface (English 🇬🇧 / Français 🇫🇷):** Instant language switcher in the navigation bar with complete translations tailored for Cameroon's official bilingualism.

---

## 🌍 Live Access Links (Any Device, Any Network)

### 1. 🌐 Public HTTPS URL (Accessible Worldwide on 4G, 5G, or any Wi-Fi):
👉 **[https://d30286483f9fb4.lhr.life](https://d30286483f9fb4.lhr.life)**
- Works on smartphones even when not on the same Wi-Fi.
- Supports native mobile browser camera permissions for the **Door Scanner**.

### 2. 📶 Local Wi-Fi Network URL:
👉 **`http://192.168.1.82:8000/`**

### 3. 💻 Localhost (Host PC):
👉 **[http://localhost:8000/](http://localhost:8000/)**

---

## 👥 Seeded Demo Accounts

You can immediately test all roles using the pre-seeded accounts:

| Role | Username | Password | Notes |
|---|---|---|---|
| **Administrator** | `admin` | `admin12345` | Access to `/admin/` and full system moderation |
| **Organizer (IAI)** | `iai_organizer` | `pass12345` | Manages Tech Summit, Football Derby & Private Marriage RSVP |
| **Organizer (Douala)** | `douala_media` | `pass12345` | Manages Douala Music Festival & Buea DevFest |
| **Attendee (Yaoundé)** | `paul_biya_student` | `pass12345` | Holds booked passes and digital QR tickets |
| **Attendee (Douala)** | `marie_douala` | `pass12345` | Holds VIP passes for Douala Festival |

---

## 🛠️ Quick Commands

```powershell
# Activate Environment
cd C:\Eventix
.\venv\Scripts\Activate.ps1

# Run Server
python manage.py runserver 0.0.0.0:8000

# Run Public HTTPS Tunnel (if needed)
ssh -o StrictHostKeyChecking=no -R 80:127.0.0.1:8000 nokey@localhost.run
```
