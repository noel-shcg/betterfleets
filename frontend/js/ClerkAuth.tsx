import {
  ClerkProvider,
  SignIn,
  SignUp,
  UserProfile,
  Show,
  UserButton,
  useClerk,
} from "@clerk/react";
import { useEffect } from "react";

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
      <a href="/accounts/login/" className="button">Sign in</a>
      <a href="/accounts/signup/" className="button">Sign up</a>
    </span>
  );
}

function AuthControls() {
  if (!publishableKey) {
    return <MissingClerkConfiguration />;
  }

  return (
    <ClerkProvider publishableKey={publishableKey}>
      <Show when="signed-out">
        <SignedOutControls />
      </Show>
      <Show when="signed-in">
        <UserButton userProfileMode="navigation" userProfileUrl="/accounts/dashboard/" />
      </Show>
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
