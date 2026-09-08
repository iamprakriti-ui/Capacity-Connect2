# CAPACITY CONNECT — Product Requirements Document

## Original problem statement
Build a production-quality web-based Learning Management System called CAPACITY CONNECT for employee skill-gap analysis, personalized learning, courses, assessments, certificates, progress tracking, and analytics across Employee, Trainer, and Administrator roles.

## Architecture decisions
- React 19 frontend with responsive CSS, Recharts visualizations, Lucide iconography, and React Router-ready page state.
- FastAPI backend with `/api` routes, seeded demo data, and server-side AI recommendations.
- MongoDB connection variables remain protected and available for the next persistence phase.
- AI recommendations use the Emergent universal LLM key through `emergentintegrations`, GPT-5.4, and streamed SSE responses with a user-friendly fallback.
- Employee workspace is the first complete vertical slice; navigation provides working foundations for the other role-specific surfaces.

## User personas
- Employee / learner: wants a clear view of capability, gaps, learning momentum, and the next best course.
- Trainer: needs to create and manage courses, learners, assessments, analytics, and certificates.
- Administrator: needs organization-wide people, skills, courses, gaps, reporting, and settings controls.

## Core requirements (static)
- Premium dark-first enterprise interface with CAPACITY CONNECT branding and “Connect Skills. Unlock Potential.” tagline.
- Seeded realistic dashboard content for capability, readiness, skills, courses, assessments, certificates, and activity.
- Responsive desktop/mobile layout with collapsible sidebar and consistent data-test IDs on user-facing interactions.
- AI-powered course insight based on a current skill gap.
- Functional navigation foundation for employee pages.

## Implemented — 2026-09-04
- Replaced starter screen with executive-style employee dashboard.
- Added seeded dashboard, courses, skills, assessments, certificates, and streamed AI API endpoints.
- Added capability score ring, readiness bars, skill map, activity chart, AI insight panel, course progress, and upcoming assessment views.
- Added responsive collapsible sidebar and workspace pages for My Skills, Skill Gaps, AI Learning, My Courses, Assessments, Certificates, Progress, and Profile.
- Added premium dark styling, typography, responsive mobile layout, animations, and interactive toast feedback for core actions.
- Verified frontend production build, public APIs, AI stream response, dashboard navigation, and 390px mobile layout.

## Prioritized backlog
### P0
- Add persistent MongoDB collections and CRUD services for users, roles, skills, courses, modules, lessons, enrollments, assessments, results, certificates, progress, and notifications.
- Add real login, registration, password recovery, JWT role access control, and role-specific route guards.

### P1
- Build trainer course authoring, learner roster, assessment builder, analytics, and certificate issuance flows.
- Build administrator people, skills, course catalog, gap reporting, analytics, reports, and settings flows.
- Add course player with lessons, video/resource support, quiz submission, and completion tracking.

### P2
- Make header search, notification center, profile menu, date filters, and export/report actions fully persistent.
- Add organization-level skill taxonomy import, manager review workflows, and scheduled capability reviews.

## Next tasks
1. Replace in-process demo constants with MongoDB-backed repositories and seed scripts.
2. Add authentication and role-specific dashboards.
3. Complete interactive course player and assessment submission flow.
4. Add trainer and administrator management surfaces.

