# Orchids Website Cloner Frontend

This is the Next.js frontend for the AI Website Cloner.

## Requirements
- Node.js 18+
- npm
- The backend server running (see backend/README.md)

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```

3. **Open your browser:**
   Visit [http://localhost:3000](http://localhost:3000)

## How it Works
- Enter a website URL in the form.
- The frontend sends the URL to the backend (`/clone`).
- The backend scrapes the site, generates HTML using Claude, and returns the result.
- The frontend displays the cloned HTML.

## Notes
- Make sure the backend is running and accessible at `http://localhost:8000` (default).
- You can adjust the backend URL in the frontend code if needed.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
