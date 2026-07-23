<template>

<Navbar />

  <div class="min-h-screen bg-slate-50 py-10 px-6">

  <div class="bg-white rounded-3xl shadow-xl p-8 max-w-3xl mx-auto">

    <h2 class="text-3xl font-bold text-center mb-2">
      Upload Voice Assessment
    </h2>

    <p class="text-center text-slate-500 mb-6">
      Please complete the voice assessment by uploading
      <strong>five recordings</strong>.
    </p>

    <!-- Instructions -->

    <div class="bg-blue-50 border border-blue-200 rounded-2xl p-5 mb-8">

      <h3 class="font-semibold text-blue-900 mb-3">
        Recording Guidelines
      </h3>

      <ul class="text-blue-800 text-sm space-y-2">
        <li>• Record in a quiet environment.</li>
        <li>• Hold each sound continuously for <strong>5–6 seconds</strong>.</li>
        <li>• Keep the microphone 10–15 cm from your mouth.</li>
        <li>• Upload one WAV recording for each phonation below.</li>
      </ul>

    </div>

    <!-- Upload Cards -->

    <div
      v-for="recording in recordings"
      :key="recording.key"
      class="border rounded-2xl p-5 mb-5 hover:border-blue-400 transition"
    >

      <div class="flex justify-between items-start">

        <div>

          <h3 class="font-semibold text-lg">
            {{ recording.label }}
          </h3>

          <p class="text-2xl font-bold text-blue-700 mt-1">
            {{ recording.sound }}
          </p>

          <p class="text-slate-600 mt-2">
            {{ recording.instruction }}
          </p>

          <p class="text-xs text-slate-400 mt-2">
            Duration: 5–6 seconds • WAV format
          </p>

        </div>

        <div
          v-if="recording.file"
          class="text-green-600 font-semibold"
        >
          ✓ Uploaded
        </div>

      </div>

      <label
        class="mt-4 flex justify-center items-center border-2 border-dashed border-blue-300 rounded-xl py-6 cursor-pointer hover:bg-blue-50 transition"
      >

        <div class="text-center">

          <div class="text-3xl">
            🎤
          </div>

          <div class="mt-2 text-blue-700 font-medium">
            Click to upload {{ recording.sound }}
          </div>

          <div class="text-xs text-slate-500 mt-1">
            WAV • 5–6 seconds
          </div>

        </div>

        <input
          class="hidden"
          type="file"
          accept=".wav,audio/wav"
          @change="handleFile($event, recording.key)"
        />

      </label>

      <p
        v-if="recording.file"
        class="text-sm text-slate-600 mt-3"
      >
        {{ recording.file.name }}
      </p>

    </div>

    <!-- Progress -->

    <div class="mb-5">

      <div class="flex justify-between text-sm text-slate-600 mb-2">
        <span>Progress</span>
        <span>{{ uploadedCount }}/5 uploaded</span>
      </div>

      <div class="w-full bg-gray-200 rounded-full h-3">

        <div
          class="bg-blue-600 h-3 rounded-full transition-all duration-300"
          :style="{ width: (uploadedCount / 5) * 100 + '%' }"
        ></div>

      </div>

    </div>

    <button
      @click="analyze"
      :disabled="!allUploaded || loading"
      class="w-full bg-blue-600 hover:bg-blue-700 text-white py-4 rounded-xl font-semibold disabled:bg-gray-300 disabled:cursor-not-allowed transition"
    >

      <span v-if="loading">
        Analyzing Assessment...
      </span>

      <span v-else>
        Analyze Assessment
      </span>

    </button>

  </div>
</div>
</template>

<script setup>
import Navbar from "../components/Navbar.vue"

import { ref, computed } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()

const loading = ref(false)

const recordings = ref([

  {
    key: "ve",
    label: "Recording 1",
    sound: "VE",
    instruction: 'Say "VEEEEEEE" continuously.',
    file: null
  },

  {
    key: "vi",
    label: "Recording 2",
    sound: "VI",
    instruction: 'Say "VIIIIIII" continuously.',
    file: null
  },

  {
    key: "vo",
    label: "Recording 3",
    sound: "VO",
    instruction: 'Say "VOOOOOOO" continuously.',
    file: null
  },

  {
    key: "vu",
    label: "Recording 4",
    sound: "VU",
    instruction: 'Say "VUUUUUU" continuously.',
    file: null
  },

  {
    key: "d2",
    label: "Recording 5",
    sound: "D2",
    instruction: 'Repeat "D2 D2 D2..." continuously.',
    file: null
  }

])

const uploadedCount = computed(() =>
  recordings.value.filter(r => r.file).length
)

const allUploaded = computed(() =>
  uploadedCount.value === 5
)

function handleFile(event, key) {

  const file = event.target.files[0]

  if (!file) return

  const recording = recordings.value.find(
    r => r.key === key
  )

  if (recording) {
    recording.file = file
  }

}

async function analyze() {

  loading.value = true

  try {

    const formData = new FormData()

    recordings.value.forEach(recording => {

      formData.append(
        recording.key,
        recording.file
      )

    })

    const response = await fetch(
      "https://voxora-46kt.onrender.com/predict",
      {
        method: "POST",
        body: formData
      }
    )

    const result = await response.json()

    if (!response.ok) {

      alert(result.detail || "Analysis failed.")

      return

    }

    console.log(result)

    router.push({

      path: "/results",

      query: {

        diagnosis: result.diagnosis,

        confidence: result.confidence

      }

    })

  }

  catch (err) {

    console.error(err)

    alert("Unable to connect to the server.")

  }

  finally {

    loading.value = false

  }

}

</script>