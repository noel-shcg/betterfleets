import {
  ClerkProvider,
  SignIn,
  SignUp,
  UserProfile,
  Show,
  UserButton,
  useUser,
  useClerk,
} from "@clerk/react";
import { useEffect } from "react";
import { createPortal } from "react-dom";

const publishableKey = process.env.VITE_CLERK_PUBLISHABLE_KEY;

function MissingClerkConfiguration() {
  return (
    <p className="clerk-auth-error">
      Clerk authentication is not configured. Set the publishable key before
      using account access.
    </p>
  );
}

function SignedOutControls() {
  return (
    <span className="clerk-auth-controls">
      <a href="/accounts/login/" className="button">Account</a>
      <a href="/accounts/signup/" className="button">Sign up</a>
    </span>
  );
}

function LoginStatus() {
  const { isLoaded, isSignedIn, user } = useUser();

  if (!isLoaded) {
    return null;
  }

  if (!isSignedIn || !user) {
    return (
      <p className="clerk-login-status">
        <a href="/accounts/login/">Sign in</a> to access your account.
      </p>
    );
  }

  const displayName =
    user.primaryEmailAddress?.emailAddress ||
    user.username ||
    user.firstName ||
    "your account";

  return (
    <p className="clerk-login-status">
      Signed in as <a href="/accounts/dashboard/">{displayName}</a>.
    </p>
  );
}

function AuthControls() {
  if (!publishableKey) {
    return <MissingClerkConfiguration />;
  }

  const footerElement = document.getElementById("clerk-login-status-root");

  return (
    <ClerkProvider publishableKey={publishableKey}>
      <Show when="signed-out">
        <SignedOutControls />
      </Show>
      <Show when="signed-in">
        <span className="clerk-auth-controls">
          <a href="/accounts/dashboard/" className="button">Account</a>
          <UserButton
            userProfileMode="navigation"
            userProfileUrl="/accounts/dashboard/"
          />
        </span>
      </Show>
      {footerElement ? createPortal(<LoginStatus />, footerElement) : null}
    </ClerkProvider>
  );
}

export default AuthControls;

export function ClerkSignIn() {
  if (!publishableKey) {
    return <MissingClerkConfiguration />;
  }

  return (
    <ClerkProvider publishableKey={publishableKey}>
      <SignIn
        routing="hash"
        fallbackRedirectUrl={document.body.dataset.clerkRedirectUrl || "/"}
      />
    </ClerkProvider>
  );
}

export function ClerkSignUp() {
  if (!publishableKey) {
    return <MissingClerkConfiguration />;
  }

  return (
    <ClerkProvider publishableKey={publishableKey}>
      <SignUp
        routing="hash"
        fallbackRedirectUrl={document.body.dataset.clerkRedirectUrl || "/"}
      />
    </ClerkProvider>
  );
}

export function ClerkAccount() {
  if (!publishableKey) {
    return <MissingClerkConfiguration />;
  }

  return (
    <ClerkProvider publishableKey={publishableKey}>
      <UserProfile routing="hash" />
    </ClerkProvider>
  );
}

function ClerkSignOutAction() {
  const { signOut } = useClerk();

  useEffect(() => {
    void signOut({ redirectUrl: "/" });
  }, [signOut]);

  return <p>Signing you out…</p>;
}

export function ClerkSignOut() {
  if (!publishableKey) {
    return <MissingClerkConfiguration />;
  }

  return (
    <ClerkProvider publishableKey={publishableKey}>
      <ClerkSignOutAction />
    </ClerkProvider>
  );
}
