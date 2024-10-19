backend/
└── src/
    ├── app.ts                         // Main application logic and initialization, sets up the express server and defines middleware
    ├── index.ts                       // Entry point of the application, starts the server and handles errors
    ├── interfaces/
    │   ├── agent.interface.ts          // Defines the interface for agent objects, which represent AI agents that can perform tasks
    │   ├── api.interface.ts            // Defines the interface for API objects, which represent external APIs that can be called by agents
    │   ├── auth.interface.ts           // Defines the interface for authentication-related objects, such as user credentials and tokens
    │   ├── chat.interface.ts           // Defines the interface for chat objects, which represent conversations between users and agents
    │   ├── file.interface.ts           // Defines the interface for file objects, which represent files that can be uploaded and downloaded
    │   ├── message.interface.ts        // Defines the interface for message objects, which represent individual messages within a chat
    │   ├── model.interface.ts          // Defines the interface for model objects, which represent AI models that can be used by agents
    │   ├── parameter.interface.ts      // Defines the interface for parameter objects, which represent input parameters for API calls or agent actions
    │   ├── prompt.interface.ts         // Defines the interface for prompt objects, which represent instructions or queries given to agents
    │   ├── references.interface.ts     // Defines the interface for reference objects, which represent external resources or data sources
    │   ├── task.interface.ts           // Defines the interface for task objects, which represent actions or operations that agents can perform
    │   ├── taskResult.interface.ts     // Defines the interface for task result objects, which represent the outcomes of agent tasks
    │   ├── urlReference.interface.ts   // Defines the interface for URL reference objects, which represent links to external websites or resources
    │   └── user.interface.ts           // Defines the interface for user objects, which represent users of the application
    ├── middleware/
    │   ├── admin.middleware.ts         // Middleware for handling requests that require administrator privileges
    │   ├── auth.middleware.ts          // Middleware for handling authentication and authorization of users
    │   ├── corsConfig.middleware.ts    // Middleware for configuring Cross-Origin Resource Sharing (CORS)
    │   └── logging.middleware.ts       // Middleware for logging requests and responses
    ├── models/
    │   ├── agent.model.ts              // Defines the Mongoose schema and model for agent objects
    │   ├── api.model.ts                // Defines the Mongoose schema and model for API objects
    │   ├── chat.model.ts               // Defines the Mongoose schema and model for chat objects
    │   ├── file.model.ts               // Defines the Mongoose schema and model for file objects
    │   ├── index.ts                    // Exports all models from the models directory
    │   ├── message.model.ts            // Defines the Mongoose schema and model for message objects
    │   ├── model.model.ts              // Defines the Mongoose schema and model for model objects
    │   ├── parameter.model.ts          // Defines the Mongoose schema and model for parameter objects
    │   ├── prompt.model.ts             // Defines the Mongoose schema and model for prompt objects
    │   ├── reference.model.ts          // Defines the Mongoose schema and model for reference objects
    │   ├── task.model.ts               // Defines the Mongoose schema and model for task objects
    │   ├── taskResult.model.ts         // Defines the Mongoose schema and model for task result objects
    │   ├── urlReference.model.ts       // Defines the Mongoose schema and model for URL reference objects
    │   └── user.model.ts               // Defines the Mongoose schema and model for user objects
    ├── routes/
    │   ├── agent.route.ts              // Defines API routes for managing agents
    │   ├── api.route.ts                // Defines API routes for managing APIs
    │   ├── chat.route.ts               // Defines API routes for managing chats
    │   ├── collections.route.ts        // Defines API routes for managing collections of data
    │   ├── file.route.ts               // Defines API routes for managing files
    │   ├── health.route.ts             // Defines API routes for checking the health of the application
    │   ├── lmStudio.route.ts           // Defines API routes for interacting with LM Studio
    │   ├── message.route.ts            // Defines API routes for managing messages
    │   ├── model.route.ts              // Defines API routes for managing models
    │   ├── parameter.route.ts          // Defines API routes for managing parameters
    │   ├── prompt.route.ts             // Defines API routes for managing prompts
    │   ├── task.route.ts               // Defines API routes for managing tasks
    │   ├── taskResult.route.ts         // Defines API routes for managing task results
    │   ├── urlReference.route.ts       // Defines API routes for managing URL references
    │   └── user.route.ts               // Defines API routes for managing users
    └── utils/
        ├── chat.utils.ts               // Utility functions for working with chats
        ├── file.utils.ts               // Utility functions for working with files
        ├── lmStudio.utils.ts           // Utility functions for interacting with LM Studio
        ├── lmStudioManager.ts          // Manages interactions with LM Studio
        ├── lmStudioNetworkTests.ts     // Performs network tests for LM Studio
        ├── logger.ts                   // Logger for the application
        ├── message.utils.ts            // Utility functions for working with messages
        ├── purge.utils.ts              // Utility functions for purging data
        ├── reference.utils.ts          // Utility functions for working with references
        ├── routeGenerator.ts           // Generates API routes
        ├── schemas.ts                  // Defines Zod schemas for data validation
        ├── taskResult.utils.ts         // Utility functions for working with task results
        ├── urlReference.utils.ts       // Utility functions for working with URL references
        ├── utils.d.ts                  // Type definitions for utility functions
        └── utils.ts                    // General utility functions

frontend/
├── .gitignore                         // Standard gitignore file for a Node.js project, excludes common development and build artifacts
├── Dockerfile                         // Dockerfile for building a production-ready image of the frontend, uses a multi-stage build to optimize for size
├── Dockerfile.dev                     // Dockerfile for building a development image of the frontend, sets up a development environment with hot reloading
├── README.md                          // Provides a comprehensive overview of the frontend container, its features, project structure, key components, and instructions for development, building, testing, and contributing
├── package-lock.json                  // Auto-generated file that records the exact versions of all installed npm packages and their dependencies, ensures consistent installations across different environments
├── package.json                       // Lists project metadata, dependencies, scripts, and configuration settings, used by npm to manage the project
├── postcss.config.js                  // Configuration file for PostCSS, a tool for transforming CSS with JavaScript plugins, configures Tailwind CSS and Autoprefixer
├── public/                            // Contains static assets that are served directly by the web server, includes the main HTML file, favicon, logos, manifest, and robots.txt
│   ├── index.html
│   ├── logo_alice.ico
│   ├── logo192.png
│   ├── logo512.png
│   ├── manifest.json
│   ├── robots.txt
│   └── content/
│       └── img/
├── resolve-module.js                  // Resolves the module path for 'tailwindcss/lib/util/flattenColorPalette' using TypeScript's module resolution mechanism, ensures that the correct module is loaded
├── src/                               // Contains the source code of the frontend application, organized into components, pages, contexts, services, types, and utils
│   ├── App.tsx                        // Main application component, responsible for routing and rendering the application's layout and pages. It also handles navigation guards and provides context for authentication, API calls, notifications, and dialogs.
│   ├── Theme.ts                       // Defines the application's theme using Material UI's createTheme function. It sets the color palette to dark mode and specifies font families for different typography elements.
│   ├── assets/                        // Contains static assets such as fonts and images used throughout the application.
│   │   └── img/
│   ├── components/                    // Contains reusable UI components used across different parts of the application.
│   │   └── enhanced/
│   ├── contexts/                      // Contains React context providers for managing global state and data, such as authentication, API interactions, notifications, and dialogs.
│   │   ├── ApiContext.tsx
│   │   ├── AuthContext.tsx
│   │   ├── CardDialogContext.tsx
│   │   ├── ChatContext.tsx
│   │   ├── DialogCustomContext.tsx
│   │   ├── NotificationContext.tsx
│   │   └── TaskContext.tsx
│   ├── index.css                      // Global stylesheet for the application, including Tailwind CSS directives and custom styles.
│   ├── index.tsx                      // Entry point of the application, renders the App component and sets up the React router.
│   ├── layouts/                       // Contains layout components that define the overall structure of the application, such as the main layout and protected routes.
│   │   ├── ErrorBoundary.tsx
│   │   ├── ProtectedRoute.tsx
│   │   └── main_layout/
│   ├── logo.svg                       // SVG file for the application's logo.
│   ├── pages/                         // Contains page components that represent different views or sections of the application, such as the home page, chat page, and task creation page.
│   │   └── ChatAlice.tsx
│   ├── reportWebVitals.js             // Script for measuring and reporting web vitals, such as performance metrics.
│   ├── services/
│   ├── styles/
│   ├── types/
│   └── utils/
├── tailwind.config.js                 // Configuration file for Tailwind CSS, a utility-first CSS framework, defines custom styles, animations, and color variables
├── tailwind.config.ts                 // TypeScript version of the Tailwind CSS configuration file, provides type checking and autocompletion for Tailwind classes
└── tsconfig.json                      // Configuration file for TypeScript, specifies compiler options, include and exclude paths, and plugin configurations

workflow/
├── .gitignore                         // Specifies files and directories to be ignored by Git version control
├── Dockerfile                         // Defines the container image for the workflow module
├── README.md                          // Provides documentation for the workflow module, including setup and usage instructions
├── __init__.py                        // Initializes the workflow module and exports key components
├── entrypoint.sh                      // Shell script that serves as the entry point for the Docker container
├── main.py                            // Main script that runs the workflow application
├── requirements.txt                   // Lists Python package dependencies for the workflow module
├── api_app/                           // Contains the FastAPI application for the workflow module
│   ├── __init__.py
│   ├── app.py                         // Defines the FastAPI application and its routes
│   ├── middleware/                    // Contains middleware functions for the API
│   ├── routes/                        // Defines API routes and their handlers
│   └── util/                          // Utility functions for the API application
├── core/                              // Core functionality of the workflow module
│   ├── __init__.py
│   ├── agent/                         // Implements AI agent functionality
│   ├── api/                           // Handles API integrations
│   ├── chat/                          // Manages chat functionality
│   ├── data_structures/               // Defines data structures used throughout the module
│   ├── model/                         // Implements AI model functionality
│   ├── prompt/                        // Manages prompts for AI interactions
│   └── tasks/                         // Defines and implements various tasks
├── db_app/                            // Database application for the workflow module
│   ├── __init__.py
│   ├── app/                           // Main database application logic
│   ├── initialization/                // Handles database initialization
│   └── prompts/                       // Manages prompts related to database operations
├── test/                              // Contains test files for the workflow module
│   ├── __init__.py
│   ├── component_tests/               // Tests for individual components
│   ├── test_results/                  // Stores test results
│   └── unit_tests/                    // Unit tests for the module
└── util/                              // Utility functions and constants for the workflow module
    ├── __init__.py
    ├── const.py                       // Defines constants used throughout the module
    ├── logging_config.py              // Configures logging for the module
    ├── run_code.py                    // Utility for running code snippets
    └── utils.py                       // General utility functions
