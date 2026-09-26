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
import { useEffect, useState } from "react";
import { createPortal } from "react-dom";

const buildTimePublishableKey = process.env.VITE_CLERK_PUBLISHABLE_KEY || "";
let publishableKeyPromise: Promise<string> | undefined;

function loadPublishableKey() {
  if (buildTimePublishableKey) {
    return Promise.resolve(buildTimePublishableKey);
  }

  publishableKeyPromise ??= fetch("/clerk/config/")
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Unable to load Clerk configuration (${response.status})`);
      }
      return response.json() as Promise<{ publishableKey?: string }>;
    })
    .then((config) => config.publishableKey || "");

  return publishableKeyPromise;
}

function usePublishableKey() {
  const [publishableKey, setPublishableKey] = useState<string>();
  const [configurationError, setConfigurationError] = useState<Error>();

  useEffect(() => {
    let active = true;
    void loadPublishableKey()
      .then((key) => {
        if (active) {
          setPublishableKey(key);
        }
      })
      .catch((error: unknown) => {
        if (active) {
          setConfigurationError(
            error instanceof Error
              ? error
              : new Error("Unable to load Clerk configuration"),
          );
        }
      });

    return () => {
      active = false;
    };
  }, []);

  return { configurationError, publishableKey };
}

function MissingClerkConfiguration() {
  return (
    <p className="clerk-auth-error">
      Clerk authentication is not configured. Set the publishable key before
      using account access.
    </p>
  );
}

function AccountIcon() {
  return (
    <svg
      aria-hidden="true"
      className="clerk-control-icon"
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="8" r="4" />
      <path d="M5 20c.8-3.2 3.1-5 7-5s6.2 1.8 7 5" />
    </svg>
  );
}

function SignedOutControls() {
  return (
    <span className="clerk-auth-controls">
      <a
        href="/accounts/login/"
        className="site-header__account-link"
        aria-label="Sign in"
        title="Sign in"
      >
        <AccountIcon />
      </a>
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
      <span className="clerk-login-status">
        <a href="/accounts/login/">Sign in</a> to access your account.
      </span>
    );
  }

  const displayName =
    user.primaryEmailAddress?.emailAddress ||
    user.username ||
    user.firstName ||
    "your account";

  return (
    <span className="clerk-login-status">
      Signed in as <a href="/accounts/dashboard/">{displayName}</a>.
    </span>
  );
}

function AuthControls() {
  const { configurationError, publishableKey } = usePublishableKey();

  if (configurationError) {
    return <MissingClerkConfiguration />;
  }
  if (publishableKey === undefined) {
    return null;
  }
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
          <UserButton
            appearance={{ elements: { userButtonAvatarBox: "site-header__avatar" } }}
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
  const { configurationError, publishableKey } = usePublishableKey();

  if (configurationError) {
    return <MissingClerkConfiguration />;
  }
  if (publishableKey === undefined) {
    return null;
  }
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
  const { configurationError, publishableKey } = usePublishableKey();

  if (configurationError) {
    return <MissingClerkConfiguration />;
  }
  if (publishableKey === undefined) {
    return null;
  }
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
  const { configurationError, publishableKey } = usePublishableKey();

  if (configurationError) {
    return <MissingClerkConfiguration />;
  }
  if (publishableKey === undefined) {
    return null;
  }
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
  const { configurationError, publishableKey } = usePublishableKey();

  if (configurationError) {
    return <MissingClerkConfiguration />;
  }
  if (publishableKey === undefined) {
    return null;
  }
  if (!publishableKey) {
    return <MissingClerkConfiguration />;
  }

  return (
    <ClerkProvider publishableKey={publishableKey}>
      <ClerkSignOutAction />
    </ClerkProvider>
  );
}
