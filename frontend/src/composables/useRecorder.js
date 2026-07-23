import { ref } from "vue"
import { encodeWAV } from "../utils/wavEncoder"

export function useRecorder() {

  const isRecording = ref(false)
  const recordingTime = ref(0)

  let audioContext = null
  let processor = null
  let input = null
  let analyser = null
  let stream = null

  let samples = []
  let timer = null
  let animationId = null

  async function startRecording(duration = 6000, canvas = null) {

    samples = []
    recordingTime.value = 0

    stream = await navigator.mediaDevices.getUserMedia({
      audio: true
    })

    audioContext = new AudioContext({
      sampleRate: 16000
    })

    input = audioContext.createMediaStreamSource(stream)

    analyser = audioContext.createAnalyser()
    analyser.fftSize = 2048

    processor = audioContext.createScriptProcessor(
      4096,
      1,
      1
    )

    // microphone
    input.connect(analyser)

    // analyser -> processor
    analyser.connect(processor)

    // processor -> output
    processor.connect(audioContext.destination)

    processor.onaudioprocess = (event) => {

      const channel =
        event.inputBuffer.getChannelData(0)

      samples.push(
        new Float32Array(channel)
      )

    }

    isRecording.value = true

    if (canvas) {
      drawWaveform(canvas)
    }

    timer = setInterval(() => {

      recordingTime.value += 0.1

    }, 100)

    await new Promise(resolve =>
      setTimeout(resolve, duration)
    )

    clearInterval(timer)

    return stopRecording()

  }

  function stopRecording() {

    isRecording.value = false

    if (animationId) {
      cancelAnimationFrame(animationId)
    }

    processor.disconnect()
    analyser.disconnect()
    input.disconnect()

    stream.getTracks().forEach(track =>
      track.stop()
    )

    const length = samples.reduce(
      (sum, chunk) => sum + chunk.length,
      0
    )

    const merged = new Float32Array(length)

    let offset = 0

    samples.forEach(chunk => {

      merged.set(chunk, offset)

      offset += chunk.length

    })

    const blob = encodeWAV(
      merged,
      audioContext.sampleRate
    )

    audioContext.close()

    return blob

  }

  function drawWaveform(canvas) {

    if (!canvas || !analyser) return

    const ctx = canvas.getContext("2d")

    const bufferLength = analyser.fftSize
    const dataArray = new Uint8Array(bufferLength)

    function draw() {

      animationId = requestAnimationFrame(draw)

      analyser.getByteTimeDomainData(dataArray)

      ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
      )

      ctx.fillStyle = "#0f172a"
      ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
      )

      ctx.lineWidth = 2
      ctx.strokeStyle = "#3b82f6"

      ctx.beginPath()

      const sliceWidth =
        canvas.width / bufferLength

      let x = 0

      for (let i = 0; i < bufferLength; i++) {

        const v = dataArray[i] / 128
        const y =
          (v * canvas.height) / 2

        if (i === 0) {
          ctx.moveTo(x, y)
        } else {
          ctx.lineTo(x, y)
        }

        x += sliceWidth

      }

      ctx.stroke()

    }

    draw()

  }

  return {

    startRecording,
    isRecording,
    recordingTime

  }

}