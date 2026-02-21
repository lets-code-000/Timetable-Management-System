<script lang="ts">
  import { goto } from "$app/navigation";
  import { PUBLIC_API_BASE_URL } from "$env/static/public";
  import { CalendarDays, Users, BookOpen, GraduationCap } from 'lucide-svelte';

  // --- Common state ---
  let showLogin = $state(true); // true = show login by default

  // Login state
  let loginEmail = $state("");
  let loginPassword = $state("");
  let loginError = $state("");
  let loginLoading = $state(false);

  // Register state
  let regUsername = $state("");
  let regEmail = $state("");
  let regPassword = $state("");
  let regCollegeId = $state("");
  let regError = $state("");
  let regSuccess = $state("");
  let regLoading = $state(false);

  // Colleges for registration dropdown
  let colleges: { id: number; name: string }[] = $state([]);
  let collegesLoaded = $state(false);

  async function loadColleges() {
    if (collegesLoaded) return;
    try {
      const res = await fetch(`${PUBLIC_API_BASE_URL}/college/public`);
      if (res.ok) {
        colleges = await res.json();
      }
    } catch {
      // Colleges will remain empty — user can still register without one
    }
    collegesLoaded = true;
  }

  // --- Login Function ---
  async function loginUser(event: Event) {
    event.preventDefault();
    loginError = "";
    loginLoading = true;
    const formData = new URLSearchParams();
    formData.append("username", loginEmail);
    formData.append("password", loginPassword);

    try {
      const res = await fetch(`${PUBLIC_API_BASE_URL}/auth/login`, {
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
    } finally {
      loginLoading = false;
    }
  }

  // --- Register Function ---
  async function registerUser(event: Event) {
    event.preventDefault();
    regError = "";
    regSuccess = "";
    regLoading = true;

    // simple client-side email check to avoid 422 roundtrip
    const basicEmailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regEmail || !basicEmailRegex.test(regEmail)) {
      regError = "Please enter a valid email address.";
      regLoading = false;
      return;
    }

    const user: Record<string, unknown> = {
      username: regUsername,
      email: regEmail,
      password: regPassword
    };
    if (regCollegeId) {
      user.college_id = Number(regCollegeId);
    }

    try {
      const res = await fetch(`${PUBLIC_API_BASE_URL}/auth/register`, {
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
      regCollegeId = "";
      showLogin = true; // automatically show login after successful registration
    } catch (err: unknown) {
      if (err instanceof Error) regError = err.message;
      else regError = String(err);
    } finally {
      regLoading = false;
    }
  }

  function toggleForm() {
    showLogin = !showLogin;
    if (!showLogin) {
      loadColleges();
    }
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 flex">
  <!-- Left side - Hero section -->
  <div class="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-blue-600 to-indigo-700 p-12 flex-col justify-center relative overflow-hidden">
    <div class="absolute inset-0 bg-black/10"></div>
    <div class="relative z-10 text-white">
      <div class="mb-8">
        <CalendarDays class="w-16 h-16 mb-4 text-blue-200" />
        <h1 class="text-4xl font-bold mb-4">TimetableIQ</h1>
        <p class="text-xl text-blue-100 leading-relaxed">
          Smart timetable management system for educational institutions.
          Streamline scheduling, optimize resources, and enhance productivity.
        </p>
      </div>

      <div class="grid grid-cols-2 gap-6 mt-12">
        <div class="flex items-center space-x-3">
          <Users class="w-8 h-8 text-blue-200" />
          <div>
            <h3 class="font-semibold">User Management</h3>
            <p class="text-sm text-blue-100">Manage faculty, students & staff</p>
          </div>
        </div>
        <div class="flex items-center space-x-3">
          <BookOpen class="w-8 h-8 text-blue-200" />
          <div>
            <h3 class="font-semibold">Subject Planning</h3>
            <p class="text-sm text-blue-100">Organize curriculum efficiently</p>
          </div>
        </div>
        <div class="flex items-center space-x-3">
          <GraduationCap class="w-8 h-8 text-blue-200" />
          <div>
            <h3 class="font-semibold">Faculty Scheduling</h3>
            <p class="text-sm text-blue-100">Optimize teaching assignments</p>
          </div>
        </div>
        <div class="flex items-center space-x-3">
          <CalendarDays class="w-8 h-8 text-blue-200" />
          <div>
            <h3 class="font-semibold">Timetable Generation</h3>
            <p class="text-sm text-blue-100">Automated conflict-free schedules</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Decorative elements -->
    <div class="absolute top-20 right-20 w-32 h-32 bg-white/10 rounded-full blur-xl"></div>
    <div class="absolute bottom-20 left-20 w-24 h-24 bg-blue-300/20 rounded-full blur-lg"></div>
  </div>

  <!-- Right side - Auth forms -->
  <div class="w-full lg:w-1/2 flex items-center justify-center p-8">
    <div class="w-full max-w-md">
      <!-- Logo for mobile -->
      <div class="lg:hidden text-center mb-8">
        <CalendarDays class="w-12 h-12 mx-auto mb-4 text-blue-600" />
        <h1 class="text-3xl font-bold text-gray-900">TimetableIQ</h1>
      </div>

      <div class="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
        {#if showLogin}
          <!-- --- LOGIN FORM --- -->
          <div class="text-center mb-8">
            <h2 class="text-3xl font-bold text-gray-900 mb-2">Welcome Back</h2>
            <p class="text-gray-600">Sign in to your account</p>
          </div>

          {#if loginError}
            <div class="bg-red-50 border border-red-200 text-red-700 p-4 mb-6 rounded-xl flex items-center space-x-2">
              <div class="w-5 h-5 bg-red-500 rounded-full flex items-center justify-center">
                <span class="text-white text-xs">!</span>
              </div>
              <span class="text-sm">{loginError}</span>
            </div>
          {/if}

          <form onsubmit={loginUser} class="space-y-6">
            <div>
              <label for="loginEmail" class="block text-sm font-medium text-gray-700 mb-2">
                Email Address
              </label>
              <input
                id="loginEmail"
                type="email"
                placeholder="Enter your email"
                bind:value={loginEmail}
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              />
            </div>

            <div>
              <label for="loginPassword" class="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                id="loginPassword"
                type="password"
                placeholder="Enter your password"
                bind:value={loginPassword}
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              />
            </div>

            <button
              type="submit"
              disabled={loginLoading}
              class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-3 px-4 rounded-xl hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {#if loginLoading}
                <div class="flex items-center justify-center space-x-2">
                  <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Signing in...</span>
                </div>
              {:else}
                Sign In
              {/if}
            </button>
          </form>

          <div class="mt-8 text-center">
            <p class="text-gray-600">
              Don't have an account?
              <button
                type="button"
                class="text-blue-600 hover:text-blue-700 font-medium hover:underline transition-colors"
                onclick={toggleForm}
              >
                Create one
              </button>
            </p>
          </div>

        {:else}
          <!-- --- REGISTER FORM --- -->
          <div class="text-center mb-8">
            <h2 class="text-3xl font-bold text-gray-900 mb-2">Create Account</h2>
            <p class="text-gray-600">Join TimetableIQ today</p>
          </div>

          {#if regError}
            <div class="bg-red-50 border border-red-200 text-red-700 p-4 mb-6 rounded-xl flex items-center space-x-2">
              <div class="w-5 h-5 bg-red-500 rounded-full flex items-center justify-center">
                <span class="text-white text-xs">!</span>
              </div>
              <span class="text-sm">{regError}</span>
            </div>
          {/if}

          {#if regSuccess}
            <div class="bg-green-50 border border-green-200 text-green-700 p-4 mb-6 rounded-xl flex items-center space-x-2">
              <div class="w-5 h-5 bg-green-500 rounded-full flex items-center justify-center">
                <span class="text-white text-xs">✓</span>
              </div>
              <span class="text-sm">{regSuccess}</span>
            </div>
          {/if}

          <form onsubmit={registerUser} class="space-y-6">
            <div>
              <label for="regUsername" class="block text-sm font-medium text-gray-700 mb-2">
                Username
              </label>
              <input
                id="regUsername"
                type="text"
                placeholder="Choose a username"
                bind:value={regUsername}
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
              />
            </div>

            <div>
              <label for="regEmail" class="block text-sm font-medium text-gray-700 mb-2">
                Email Address
              </label>
              <input
                id="regEmail"
                type="email"
                placeholder="Enter your email"
                bind:value={regEmail}
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
              />
            </div>

            <div>
              <label for="regPassword" class="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                id="regPassword"
                type="password"
                placeholder="Create a password"
                bind:value={regPassword}
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
              />
            </div>

            <div>
              <label for="regCollege" class="block text-sm font-medium text-gray-700 mb-2">
                College (Optional)
              </label>
              <select
                id="regCollege"
                bind:value={regCollegeId}
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
              >
                <option value="">Select your college</option>
                {#each colleges as college}
                  <option value={college.id}>{college.name}</option>
                {/each}
              </select>
            </div>

            <button
              type="submit"
              disabled={regLoading}
              class="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white py-3 px-4 rounded-xl hover:from-green-700 hover:to-emerald-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-all duration-200 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {#if regLoading}
                <div class="flex items-center justify-center space-x-2">
                  <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Creating account...</span>
                </div>
              {:else}
                Create Account
              {/if}
            </button>
          </form>

          <div class="mt-8 text-center">
            <p class="text-gray-600">
              Already have an account?
              <button
                type="button"
                class="text-blue-600 hover:text-blue-700 font-medium hover:underline transition-colors"
                onclick={toggleForm}
              >
                Sign in
              </button>
            </p>
          </div>
        {/if}
      </div>
    </div>
  </div>
</div>