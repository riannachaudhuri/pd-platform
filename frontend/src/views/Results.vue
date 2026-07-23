<template>

  <Navbar />

  <div class="min-h-screen bg-slate-100 py-10 px-6">

    <div class="bg-white rounded-3xl shadow-2xl w-full max-w-3xl mx-auto overflow-hidden">

      <!-- Header -->

      <div class="bg-blue-600 text-white p-8">

        <h1 class="text-3xl font-bold">
          Voice Assessment Results
        </h1>

        <p class="mt-2 text-blue-100">
          AI-assisted Parkinson's Disease Screening
        </p>

      </div>

      <!-- Body -->

      <div class="p-10">

        <!-- Diagnosis -->

        <div class="text-center">

          <div
            class="w-32 h-32 rounded-full mx-auto flex items-center justify-center text-6xl"
            :class="diagnosis == 'Healthy'
              ? 'bg-green-100'
              : 'bg-red-100'"
          >

            {{ diagnosis == "Healthy" ? "✓" : "⚠" }}

          </div>

          <h2
            class="mt-6 text-4xl font-bold"
            :class="diagnosis == 'Healthy'
              ? 'text-green-600'
              : 'text-red-600'"
          >
            {{ diagnosis }}
          </h2>

          <p class="text-slate-500 mt-2">
            Overall AI Assessment
          </p>

        </div>

        <!-- Confidence -->

        <div class="mt-12">

          <div class="flex justify-between mb-3">

            <span class="font-semibold">
              Confidence
            </span>

            <span class="font-bold text-lg">
              {{ confidence }}%
            </span>

          </div>

          <div class="w-full bg-gray-200 rounded-full h-5">

            <div
              class="h-5 rounded-full transition-all duration-1000"
              :class="diagnosis == 'Healthy'
                ? 'bg-green-500'
                : 'bg-red-500'"
              :style="{ width: confidence + '%' }"
            ></div>

          </div>

        </div>

        <!-- Summary -->

        <div class="mt-12 bg-slate-50 rounded-2xl p-6 border">

          <h3 class="font-bold text-xl mb-3">
            Assessment Summary
          </h3>

          <p class="text-slate-600 leading-7">

            Your voice assessment was completed using
            five guided phonation recordings
            (VE, VI, VO, VU and D2).

            Each recording was analysed independently,
            after which a weighted voting algorithm
            generated the final assessment shown above.

          </p>

        </div>

        <!-- Disclaimer -->

        <div
          class="mt-8 border border-yellow-300 bg-yellow-50 rounded-2xl p-6"
        >

          <h3 class="font-semibold text-yellow-800 mb-2">
            Clinical Disclaimer
          </h3>

          <p class="text-sm text-slate-700 leading-6">

            This application is intended solely as a
            screening tool and should not be used as a
            substitute for professional medical diagnosis.

            If you have concerns regarding Parkinson's
            disease or other neurological conditions,
            please consult a qualified healthcare professional.

          </p>

        </div>

        <!-- Buttons -->

        <div class="grid grid-cols-2 gap-4 mt-10">

          <button
            class="bg-blue-600 hover:bg-blue-700 text-white py-4 rounded-xl font-semibold transition"
          >
            Download Report
          </button>

          <button
            @click="startAgain"
            class="border border-slate-300 hover:bg-slate-100 py-4 rounded-xl font-semibold transition"
          >
            New Assessment
          </button>

        </div>

      </div>

    </div>

  </div>

</template>

<script setup>

import Navbar from "../components/Navbar.vue"

import { useRoute, useRouter } from "vue-router"

const route = useRoute()

const router = useRouter()

const diagnosis = route.query.diagnosis || "Unknown"

const confidence = route.query.confidence || 0

function startAgain() {

  router.push("/")

}

</script>