import { createRouter, createWebHistory } from "vue-router"

import Home from "../views/Home.vue"
import RecordingAssessment from "../views/RecordingAssessment.vue"
import UploadCard from "../views/UploadCard.vue"
import Results from "../views/Results.vue"

const router = createRouter({
  history: createWebHistory(),

  routes: [
    {
      path: "/",
      component: Home
    },
    {
      path: "/record",
      component: RecordingAssessment
    },
    {
      path: "/upload",
      component: UploadCard
    },
    {
      path: "/results",
      component: Results
    }
  ]
})

export default router