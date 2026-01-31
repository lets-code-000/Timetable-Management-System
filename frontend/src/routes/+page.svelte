<script lang="ts">
  import { goto } from "$app/navigation";

  // --- Common state ---
  let showLogin = $state(true); // true = show login by default

  // Login state
  let loginEmail = $state("");
  let loginPassword = $state("");
  let loginError = $state("");

  // Register state
  let regUsername = $state("");
  let regEmail = $state("");
  let regPassword = $state("");
  let regError = $state("");
  let regSuccess = $state("");

  // --- Login Function ---
  async function loginUser() {
    loginError = "";
    const formData = new URLSearchParams();
    formData.append("username", loginEmail);
    formData.append("password", loginPassword);

    try {
      const res = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData
      });

      if (!res.ok) {
        const data = await res.json();
        loginError = data.detail || "Login failed";
        return;
      }

      const data = await res.json();
      
      // Store token in cookie instead of localStorage for server-side access
      document.cookie = `token=${data.access_token}; path=/; max-age=${60 * 60 * 24 * 7}`; // 7 days
      
      // Redirect to dashboard and invalidate all to refresh server-side state
      goto("/dashboard", { invalidateAll: true });
    } catch (err: unknown) {
      if (err instanceof Error) loginError = err.message;
      else loginError = String(err);
    }
  }

  // --- Register Function ---
  async function registerUser() {
    regError = "";
    regSuccess = "";

    // simple client-side email check to avoid 422 roundtrip
    const basicEmailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regEmail || !basicEmailRegex.test(regEmail)) {
      regError = "Please enter a valid email address.";
      return;
    }

    const user = {
      username: regUsername,
      email: regEmail,
      password: regPassword
    };

    try {
      const res = await fetch("http://localhost:8000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(user)
      });

      if (!res.ok) {
        const data = await res.json();
        // FastAPI may return {detail: "..."} or {detail: [{msg: "..."}, ...]}
        let message = "Registration failed";
        if (data?.detail) {
          if (typeof data.detail === "string") message = data.detail;
          else if (Array.isArray(data.detail) && data.detail.length) {
            message = data.detail.map((e: any) => e.msg || e.detail || "").filter(Boolean).join("; ") || message;
          }
        }
        regError = message;
        return;
      }

      regSuccess = "✅ Registration successful! You can now login.";
      // Clear fields
      regUsername = "";
      regEmail = "";
      regPassword = "";
      showLogin = true; // automatically show login after successful registration
    } catch (err: unknown) {
      if (err instanceof Error) regError = err.message;
      else regError = String(err);
    }
  }

  function toggleForm() {
    showLogin = !showLogin;
  }
</script>

<div class="min-h-screen flex items-center justify-center bg-gray-100">
  <div class="bg-white p-8 rounded shadow-md w-full max-w-md">
    <h1 class="text-3xl font-bold mb-6 text-center" style="font-family: 'Poppins', sans-serif;">
      Welcome to TimetableIQ
    </h1>

    {#if showLogin}
      <!-- --- LOGIN FORM --- -->
      <h2 class="text-2xl font-semibold mb-4 text-center">Login</h2>

      {#if loginError}
        <div class="bg-red-100 text-red-700 p-2 mb-4 rounded">{loginError}</div>
      {/if}

      <input
        type="email"
        placeholder="Email"
        bind:value={loginEmail}
        class="w-full p-3 mb-4 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      <input
        type="password"
        placeholder="Password"
        bind:value={loginPassword}
        class="w-full p-3 mb-4 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      <button
        onclick={loginUser}
        class="w-full bg-blue-500 text-white py-3 rounded hover:bg-blue-600 transition-colors mb-2"
      >
        Login
      </button>

      <p class="text-sm text-center text-gray-600 mt-2">
        Don't have an account?
        <button type="button" class="text-blue-500 cursor-pointer hover:underline" onclick={toggleForm}>Register here</button>
      </p>

    {:else}
      <!-- --- REGISTER FORM --- -->
      <h2 class="text-2xl font-semibold mb-4 text-center">Register</h2>

      {#if regError}
        <div class="bg-red-100 text-red-700 p-2 mb-4 rounded">{regError}</div>
      {/if}
      {#if regSuccess}
        <div class="bg-green-100 text-green-700 p-2 mb-4 rounded">{regSuccess}</div>
      {/if}

      <input
        type="text"
        placeholder="Username"
        bind:value={regUsername}
        class="w-full p-3 mb-4 border rounded focus:outline-none focus:ring-2 focus:ring-green-400"
      />
      <input
        type="email"
        placeholder="Email"
        bind:value={regEmail}
        class="w-full p-3 mb-4 border rounded focus:outline-none focus:ring-2 focus:ring-green-400"
      />
      <input
        type="password"
        placeholder="Password"
        bind:value={regPassword}
        class="w-full p-3 mb-4 border rounded focus:outline-none focus:ring-2 focus:ring-green-400"
      />
      <button
        onclick={registerUser}
        class="w-full bg-green-500 text-white py-3 rounded hover:bg-green-600 transition-colors mb-2"
      >
        Register
      </button>

      <p class="text-sm text-center text-gray-600 mt-2">
        Already have an account?
        <button type="button" class="text-blue-500 cursor-pointer hover:underline" onclick={toggleForm}>Login here</button>
      </p>
    {/if}
  </div>
</div>