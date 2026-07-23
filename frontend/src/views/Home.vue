<template>

  <Navbar />

  <div class="min-h-screen bg-slate-50">

    <!-- Hero -->

    <section
      class="bg-gradient-to-br from-blue-700 via-blue-600 to-sky-500 text-white pb-36"
    >

      <div class="max-w-7xl mx-auto px-8 py-24">

        <div class="max-w-3xl">

          <div
            class="inline-flex items-center px-4 py-2 rounded-full bg-white/15 backdrop-blur-sm text-sm font-medium mb-8"
          >
            AI-Assisted Parkinson's Disease Screening
          </div>

          <h1
            class="text-6xl font-black tracking-tight leading-tight"
          >
            VOXORA
          </h1>

          <h2
            class="text-3xl font-light mt-5 leading-snug"
          >
            Voice Intelligence for
            Parkinson's Disease Detection
          </h2>

          <p
            class="mt-8 text-xl text-blue-100 leading-9 max-w-2xl"
          >
            A clinical decision-support platform that analyzes
            sustained voice recordings using machine learning
            to assist in early Parkinson's disease screening.
          </p>

        </div>

      </div>

    </section>

    <!-- Action Cards -->

    <section class="-mt-20 relative z-20">

      <div class="max-w-7xl mx-auto px-8">

        <div class="grid lg:grid-cols-2 gap-8">

          <!-- Recording Card -->

          <div
            class="bg-white rounded-3xl shadow-xl p-10 hover:shadow-2xl hover:-translate-y-1 transition duration-300"
          >

            <div
              class="w-16 h-16 rounded-2xl bg-blue-100 flex items-center justify-center"
            >
              <Mic class="w-8 h-8 text-blue-600" />
            </div>

            <h2 class="text-3xl font-bold mt-8">
              Start Assessment
            </h2>

            <p class="text-slate-600 mt-5 leading-8">

              Complete a guided voice assessment
              directly in your browser.

              The application will guide you through
              five voice recordings automatically.

            </p>

            <button
              @click="router.push('/record')"
              class="mt-10 w-full bg-blue-600 hover:bg-blue-700 text-white py-4 rounded-2xl font-semibold text-lg transition"
            >
              Begin Assessment
            </button>

          </div>

          <!-- Upload Card -->

          <div
            class="bg-white rounded-3xl shadow-xl p-10 hover:shadow-2xl hover:-translate-y-1 transition duration-300"
          >

            <div
              class="w-16 h-16 rounded-2xl bg-sky-100 flex items-center justify-center"
            >
              <Upload class="w-8 h-8 text-sky-600" />
            </div>

            <h2 class="text-3xl font-bold mt-8">
              Upload Recordings
            </h2>

            <p class="text-slate-600 mt-5 leading-8">

              Already have your five WAV recordings?

              Upload them directly and receive an
              AI-generated Parkinson's disease assessment.

            </p>

            <button
              @click="router.push('/upload')"
              class="mt-10 w-full border-2 border-blue-600 text-blue-600 hover:bg-blue-50 py-4 rounded-2xl font-semibold text-lg transition"
            >
              Upload Files
            </button>

          </div>

        </div>

      </div>

    </section>

    <!-- Why VOXORA -->

<section class="py-24">

  <div class="max-w-7xl mx-auto px-8">

    <div class="text-center mb-16">

      <h2 class="text-4xl font-bold text-slate-800">
        Why Choose VOXORA?
      </h2>

      <p class="text-slate-500 mt-4 text-lg">
        Designed for efficient, consistent and accessible voice-based screening.
      </p>

    </div>

    <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">

      <!-- Card -->

      <div class="bg-white rounded-3xl shadow-lg p-8 text-center">

        <Brain class="w-10 h-10 text-blue-600 mx-auto"/>

        <h3 class="font-bold text-xl mt-6">
          AI Analysis
        </h3>

        <p class="text-slate-600 mt-3 leading-7">
          Machine learning evaluates voice biomarkers associated with Parkinson's disease.
        </p>

      </div>

      <div class="bg-white rounded-3xl shadow-lg p-8 text-center">

        <Mic class="w-10 h-10 text-blue-600 mx-auto"/>

        <h3 class="font-bold text-xl mt-6">
          Five Voice Samples
        </h3>

        <p class="text-slate-600 mt-3 leading-7">
          Multiple phonations improve robustness and reduce variability.
        </p>

      </div>

      <div class="bg-white rounded-3xl shadow-lg p-8 text-center">

        <ClipboardCheck class="w-10 h-10 text-blue-600 mx-auto"/>

        <h3 class="font-bold text-xl mt-6">
          Clinical Support
        </h3>

        <p class="text-slate-600 mt-3 leading-7">
          Provides clinicians with an additional screening tool for assessment.
        </p>

      </div>

      <div class="bg-white rounded-3xl shadow-lg p-8 text-center">

        <Activity class="w-10 h-10 text-blue-600 mx-auto"/>

        <h3 class="font-bold text-xl mt-6">
          Instant Results
        </h3>

        <p class="text-slate-600 mt-3 leading-7">
          Receive AI predictions immediately after completing the assessment.
        </p>

      </div>

    </div>

  </div>

</section>

<Footer />

  </div>

</template>

<script setup>

import Navbar from "../components/Navbar.vue"
import Footer from "../components/Footer.vue"

import { useRouter } from "vue-router"

import {
  Mic,
  Upload
} from "lucide-vue-next"

const router = useRouter()

</script>