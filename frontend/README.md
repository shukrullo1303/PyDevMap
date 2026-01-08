# OSMark LMS - Complete Frontend

A modern, fully-responsive Learning Management System (LMS) frontend built with React, featuring pixel-perfect design system, comprehensive course management, and interactive quiz functionality.

## 🎯 Features

- **📚 Course Management**: Browse, search, and enroll in courses with detailed course information
- **🎓 Lessons & Progress Tracking**: Learn through structured lessons with progress indicators
- **✅ Interactive Quizzes**: Take quizzes with instant scoring and detailed feedback
- **👤 User Authentication**: Secure login/register with JWT token refresh
- **📊 User Dashboard**: Track enrollments, progress, and learning statistics
- **🎨 Modern UI**: Built with semantic design tokens and responsive CSS
- **🔐 Protected Routes**: Authentication context with automatic token refresh
- **📱 Mobile Responsive**: Fully optimized for all screen sizes

## 🏗️ Architecture

### Frontend Stack
- **React 18**: Modern component-based UI framework
- **React Router v6**: Client-side routing with nested routes
- **Axios**: HTTP client with interceptors for auth token refresh
- **CSS Custom Properties**: Design tokens system for consistent styling

### Key Structure
```
src/
├── components/          # Reusable UI components
│   ├── Navbar.js        # Main navigation bar
│   ├── CourseCard.js    # Course preview card
│   ├── LessonCard.js    # Lesson item in lists
│   ├── Quiz.js          # Quiz interface with navigation
│   └── AnswerOption.js  # Quiz answer option with styling
├── pages/               # Full page components
│   ├── HomePage.js      # Course discovery landing page
│   ├── CoursePage.js    # Course details with lessons
│   ├── LessonPage.js    # Lesson content viewer
│   ├── QuizPage.js      # Quiz taker with results
│   ├── LoginPage.js     # Authentication
│   ├── RegisterPage.js  # User registration
│   └── ProfilePage.js   # User profile & enrollments
├── context/             # Global state management
│   └── AuthContext.js   # Auth state with login/register/logout
├── services/            # API integration layer
│   ├── api.js           # Axios client with token refresh
│   ├── auth.js          # Authentication endpoints
│   ├── courses.js       # Course API calls
│   ├── lessons.js       # Lesson API calls
│   ├── quiz.js          # Quiz API calls
│   └── enrollments.js   # Enrollment API calls
├── styles/
│   ├── theme.css        # Global styles using design tokens
│   └── tokens.css       # CSS design system variables
├── App.js               # Root router component
└── index.js             # React entry point
```

## 🚀 Quick Start

### Prerequisites
- Node.js 16+
- npm or yarn
- Django backend running on http://localhost:8000

### Installation

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Start development server**
```bash
npm start
```

The app will open at `http://localhost:3001`

3. **Build for production**
```bash
npm run build
```

## 🔧 Configuration

### Environment Variables
Create `.env` file in the `frontend/` directory:

```env
REACT_APP_API_BASE_URL=http://localhost:8000/api
REACT_APP_DEBUG=false
```

### API Base URL
The default API base is set to `http://localhost:8000/api`. Modify in `src/services/api.js`:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';
```

## 📖 Design System

### Color Palette
The design system uses CSS custom properties defined in `src/styles/tokens.css`:

```css
/* Primary Blue */
--primary-600: #2563eb
--primary-700: #1d4ed8

/* Accent Cyan */
--accent-500: #06b6d4

/* Semantic Colors */
--success-600: #16a34a
--warning-600: #d97706
--error-600: #dc2626

/* Neutral */
--neutral-900: #111827  /* text-primary */
--neutral-500: #6b7280  /* text-secondary */
```

### Typography
- **Font**: Inter (via Google Fonts)
- **Base Size**: 16px
- **Scales**: xs (12px) → 4xl (36px)

### Spacing
- **Base Unit**: 8px (1 space)
- **Scale**: xs (4px) → 4xl (64px)

### Components
All components use semantic tokens:
- `.btn` - Button styles (primary, outline, secondary)
- `.card` - Card container with hover effects
- `.form-control` - Input fields with focus states
- `.progress-bar` - Progress indicators
- `.lesson-card` - Lesson list item

## 📡 API Integration

### Authentication Flow
1. User submits login credentials → `POST /api/auth/login/`
2. Backend returns `access` and `refresh` tokens
3. Tokens stored in `localStorage`
4. Axios interceptor adds `Authorization: Bearer <token>` header
5. On 401 error, automatically refresh using `refresh` token
6. Retry original request with new token

### API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/auth/login/` | POST | User login |
| `/auth/register/` | POST | User registration |
| `/auth/profile/` | GET | Get current user |
| `/courses/courses/` | GET | List all courses |
| `/courses/courses/{id}/` | GET | Get course details |
| `/courses/enrollment/` | POST | Enroll in course |
| `/lessons/lessons/` | GET | List lessons |
| `/lessons/lessons/{id}/` | GET | Get lesson details |
| `/lessons/progress/` | POST | Mark lesson complete |
| `/quiz/quizzes/{id}/` | GET | Get quiz |
| `/quiz/submit/` | POST | Submit quiz answers |
| `/enrollments/my/` | GET | Get user enrollments |

## 🎨 Page Layouts

### HomePage
- Hero section with search bar
- Course grid with sorting/filtering
- Pagination support for large datasets
- Search functionality (client-side filtering)

### CoursePage
- Course header with enrollment button
- Sidebar with instructor info and course stats
- Lessons list organized by course
- Progress tracking

### LessonPage
- Breadcrumb navigation
- Progress indicator
- Lesson content with HTML rendering
- Mark complete button
- Quiz link if available

### QuizPage
- Quiz instructions and metadata
- Question navigator sidebar
- Multi-step quiz with progress bar
- Answer selection (radio/checkbox)
- Results display with score breakdown

### ProfilePage
- User information card
- Enrollment statistics
- List of enrolled courses with progress
- Account stats sidebar

### Auth Pages
- Centered login/register forms
- Email validation
- Password requirements
- Error messaging
- Links between pages

## 🌐 Responsive Design

### Breakpoints
- **Desktop**: 1024px+
- **Tablet**: 768px - 1023px
- **Mobile**: Below 768px

### Mobile Optimizations
- Stack navigation buttons
- Full-width search bar
- Single column layout
- Larger touch targets (min 44px)
- Reduced padding on small screens

## 🔐 Security Features

- **JWT Token Management**: Automatic refresh on expiry
- **Protected Routes**: Auth context guards unauthorized access
- **Secure Headers**: CORS enabled only for trusted origins
- **Input Validation**: Form validation before submission
- **Safe Token Storage**: localStorage (consider upgrading to secure storage)

## 📚 State Management

### AuthContext
Provides global authentication state:
```javascript
{
  user: { id, username, email, date_joined },
  isAuthenticated: boolean,
  loading: boolean,
  login(email, password),
  register(userData),
  logout(),
  refresh()
}
```

### Local Component State
- Courses and lessons stored in component state
- Pagination handled locally
- Form state managed with useState
- Search state for filtering

## 🧪 Testing

### Manual Testing Checklist
- [ ] User can register with email/password
- [ ] User can login with credentials
- [ ] User can browse all courses
- [ ] User can enroll in a course
- [ ] User can view course details and lessons
- [ ] User can complete a lesson
- [ ] User can take and submit a quiz
- [ ] User can view profile and enrollments
- [ ] User can logout
- [ ] Page is responsive on mobile/tablet/desktop

### Running Tests
```bash
npm test
```

## 📦 Deployment

### Build Production Bundle
```bash
npm run build
```

### Deploy to Static Hosting
```bash
# Using Vercel
vercel

# Using Netlify
netlify deploy --prod --dir=build

# Using GitHub Pages
npm run build
# Deploy build/ folder
```

### Environment Variables for Production
Update in production hosting platform:
```env
REACT_APP_API_BASE_URL=https://your-api-domain.com/api
REACT_APP_DEBUG=false
```

## 🐛 Troubleshooting

### CORS Errors
Ensure Django has CORS enabled:
```python
# config/settings/base.py
INSTALLED_APPS = [..., 'corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ...]
CORS_ALLOW_ALL_ORIGINS = True  # Development only
```

### Token Refresh Issues
Check that:
- `localStorage` token is valid
- Refresh endpoint returns new tokens
- Axios interceptor is configured correctly

### Page Not Found
- Verify Django API endpoints match service layer calls
- Check URL patterns in backend
- Ensure API responses match component expectations

## 🎓 Learning Resources

- [React Documentation](https://react.dev)
- [React Router](https://reactrouter.com)
- [Axios Documentation](https://axios-http.com)
- [CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/--*)
- [MDN Web Docs](https://developer.mozilla.org)

## 📄 License

This project is part of OSMark Learning Management System.

## 🤝 Contributing

To contribute:
1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API responses in browser DevTools
3. Check console for error messages
4. Verify backend is running and accessible

---

**Built with ❤️ using React**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
