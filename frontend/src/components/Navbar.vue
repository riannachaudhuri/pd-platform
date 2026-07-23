<template>
  <nav class="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200">

    <div class="max-w-7xl mx-auto px-8">

      <div class="flex items-center justify-between h-20">

        <!-- Logo -->

        <div
          class="flex items-center gap-4 cursor-pointer"
          @click="$router.push('/')"
        >

          <img
            src="@/assets/voxora-logo.png"
            alt="VOXORA"
            class="w-11 h-11 object-contain"
          />

          <div>

            <h1 class="text-2xl font-bold tracking-wide text-slate-800">
              VOXORA
            </h1>

            <p class="text-sm text-slate-500">
              Voice Intelligence
            </p>

          </div>

        </div>

        <!-- Navigation -->

        <div class="hidden md:flex items-center gap-8">

          <RouterLink
            to="/"
            class="font-medium text-slate-600 hover:text-blue-600 transition-colors duration-200"
          >
            Home
          </RouterLink>

          <RouterLink
            to="/record"
            class="font-medium text-slate-600 hover:text-blue-600 transition-colors duration-200"
          >
            Assessment
          </RouterLink>

          <RouterLink
            to="/upload"
            class="font-medium text-slate-600 hover:text-blue-600 transition-colors duration-200"
          >
            Upload
          </RouterLink>

        </div>

        <!-- Badge -->

        <div
          class="hidden md:flex items-center rounded-full bg-blue-100 px-4 py-2 text-sm font-semibold text-blue-700"
        >
          AI Powered
        </div>

      </div>

    </div>

  </nav>
</template>

<script setup>
import { RouterLink } from "vue-router"
</script>