import React from "react";
import { createRoot } from "react-dom/client";

import AuthControls, {
  ClerkAccount,
  ClerkSignIn,
  ClerkSignOut,
  ClerkSignUp,
} from "./ClerkAuth";

const rootElement = document.getElementById("clerk-auth-root");
const signInElement = document.getElementById("clerk-sign-in-root");
const signUpElement = document.getElementById("clerk-sign-up-root");
const accountElement = document.getElementById("clerk-account-root");
const signOutElement = document.getElementById("clerk-sign-out-root");

const redirectElement = document.querySelector("[data-clerk-redirect-url]");
if (redirectElement instanceof HTMLElement) {
  document.body.dataset.clerkRedirectUrl =
    redirectElement.dataset.clerkRedirectUrl || "/";
}

if (rootElement) {
  createRoot(rootElement).render(
    <React.StrictMode>
      <AuthControls />
    </React.StrictMode>,
  );
}

if (signInElement) {
  createRoot(signInElement).render(
    <React.StrictMode>
      <ClerkSignIn />
    </React.StrictMode>,
  );
  if (process.env.VITE_CLERK_PUBLISHABLE_KEY) {
    document.querySelector(".legacy-auth-form")?.remove();
  }

}

if (signUpElement) {
  createRoot(signUpElement).render(
    <React.StrictMode>
      <ClerkSignUp />
    </React.StrictMode>,
  );
}

if (accountElement) {
  createRoot(accountElement).render(
    <React.StrictMode>
      <ClerkAccount />
    </React.StrictMode>,
  );
}

if (signOutElement) {
  createRoot(signOutElement).render(
    <React.StrictMode>
      <ClerkSignOut />
    </React.StrictMode>,
  );
}
