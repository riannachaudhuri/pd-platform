<template>
  <footer class="bg-slate-900 text-slate-300 mt-24">

    <div class="max-w-7xl mx-auto px-8 py-12">

      <div class="grid md:grid-cols-3 gap-10">

        <!-- Brand -->

        <div>

          <h2 class="text-2xl font-bold text-white">
            VOXORA
          </h2>

          <p class="mt-4 leading-7">

            AI-assisted voice analysis for
            Parkinson's disease screening.

          </p>

        </div>

        <!-- Navigation -->

        <div>

          <h3 class="text-white font-semibold mb-4">
            Navigation
          </h3>

          <div class="space-y-3">

            <RouterLink to="/" class="block hover:text-white">
              Home
            </RouterLink>

            <RouterLink to="/record" class="block hover:text-white">
              Assessment
            </RouterLink>

            <RouterLink to="/upload" class="block hover:text-white">
              Upload
            </RouterLink>

          </div>

        </div>

        <!-- Disclaimer -->

        <div>

          <h3 class="text-white font-semibold mb-4">
            Clinical Notice
          </h3>

          <p class="leading-7 text-sm">

            VOXORA is intended as an AI-assisted
            screening tool only and should not
            replace clinical diagnosis by a qualified
            healthcare professional.

          </p>

        </div>

      </div>

      <div class="border-t border-slate-700 mt-10 pt-6 text-center text-sm text-slate-400">

        © 2026 VOXORA • Built using Vue.js, FastAPI & Machine Learning

      </div>

    </div>

  </footer>
</template>

<script setup>
import { RouterLink } from "vue-router"
</script>