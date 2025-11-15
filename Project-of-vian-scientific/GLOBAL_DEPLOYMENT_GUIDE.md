# Vian Scientific - Global Deployment & SEO Guide

This guide provides a complete roadmap to take your project from this development environment to a live, public website that performs well for users in **India, the USA, and worldwide**.

---

## 1. Principle: Build Once, Serve Globally

The application has been built with modern web standards, making it inherently global. The key is to deploy it correctly so that it's fast and accessible for everyone, everywhere.

-   **Development Environment (Here):** A private workshop for building and testing. It's not visible to the public or Google.
-   **Production Environment (A Live Website):** Your project hosted on a public server with a global Content Delivery Network (CDN), accessible 24/7 via a URL like `vianscientific.com`.

**You cannot deploy from here. You must use a separate hosting platform.**

---

## 2. Deploying for Global Performance (Step-by-Step)

Using a platform with a built-in **Content Delivery Network (CDN)** is the single most important step for ensuring a fast experience for users in both India and the USA. A CDN stores copies of your website in multiple locations around the world, so content is delivered from a server physically closer to the user.

We recommend **Vercel** or **Netlify**.

### Step 1: Download & Push Your Project to GitHub
1.  Download the complete source code of your project as a `.zip` file from this environment.
2.  Create a free account on [GitHub](https://github.com/) and create a new repository.
3.  Unzip your project and "push" the code to your new GitHub repository.

### Step 2: Deploy with Vercel (Recommended)
1.  **Sign Up:** Go to [Vercel.com](https://vercel.com/) and sign up with your GitHub account.
2.  **Import Project:** From your Vercel dashboard, click "Add New... -> Project" and select the GitHub repository you just created.
3.  **Configure Project:** Vercel will auto-detect the settings. They should be:
    -   **Framework Preset:** `Vite`
    -   **Build Command:** `vite build`
    -   **Output Directory:** `dist`
4.  **Add Environment Variables:** This is crucial for your API key.
    -   In your project settings on Vercel, go to "Settings" -> "Environment Variables".
    -   Add a variable named `API_KEY` and paste in your Gemini API key.
5.  **Deploy:** Click "Deploy". Vercel will build your site and deploy it to its global CDN.

---

## 3. International SEO & Configuration

The codebase has been configured for a global audience.

-   **Language Tagging:** The site explicitly declares its language as English (`lang="en"`), which helps search engines understand the content.
-   **Social Media Locale:** We've added Open Graph tags (`og:locale`) for `en_US` and `en_IN`. This provides hints to platforms like Facebook and LinkedIn about the site's relevance to users in these regions when links are shared.
-   **Generic Domain:** Using a `.com` domain is excellent for global reach as it is not tied to a specific country.

### After Deployment: Google Search Console
1.  **Go to Google Search Console:** [search.google.com/search-console](https://search.google.com/search-console)
2.  **Add Your Live URL:** Add `https://www.vianscientific.com`.
3.  **Verify Ownership:** Follow the instructions to prove you own the site.
4.  **Check International Targeting:** In the legacy tools section, there's an "International Targeting" report. Ensure no specific country is targeted, allowing Google to serve your site to users worldwide.
5.  **Request Indexing:** Use the URL Inspection tool to request that Google crawl your homepage.

---

## 4. Performance Monitoring for Global Users

After deploying, verify that your site is fast for your target audiences.

-   **Tool:** Use a tool like [GTmetrix](https://gtmetrix.com/) or [PageSpeed Insights](https://pagespeed.web.dev/).
-   **How to Test:**
    -   Run a test from a server location in **India (e.g., Mumbai)**.
    -   Run a second test from a server location in the **USA (e.g., Virginia)**.
-   **Goal:** Thanks to the CDN, the load times should be fast in both locations.

By following this guide, you will have a professionally deployed, SEO-optimized website that is fast, reliable, and accessible to your users in India, the USA, and across the globe.