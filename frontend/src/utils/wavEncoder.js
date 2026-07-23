export function encodeWAV(samples, sampleRate) {

  const buffer = new ArrayBuffer(44 + samples.length * 2)

  const view = new DataView(buffer)

  function writeString(offset, string) {

    for (let i = 0; i < string.length; i++) {

      view.setUint8(offset + i, string.charCodeAt(i))

    }

  }

  let offset = 0

  writeString(offset, "RIFF")
  offset += 4

  view.setUint32(
    offset,
    36 + samples.length * 2,
    true
  )
  offset += 4

  writeString(offset, "WAVE")
  offset += 4

  writeString(offset, "fmt ")
  offset += 4

  view.setUint32(offset, 16, true)
  offset += 4

  view.setUint16(offset, 1, true)
  offset += 2

  view.setUint16(offset, 1, true)
  offset += 2

  view.setUint32(offset, sampleRate, true)
  offset += 4

  view.setUint32(
    offset,
    sampleRate * 2,
    true
  )
  offset += 4

  view.setUint16(offset, 2, true)
  offset += 2

  view.setUint16(offset, 16, true)
  offset += 2

  writeString(offset, "data")
  offset += 4

  view.setUint32(
    offset,
    samples.length * 2,
    true
  )
  offset += 4

  for (let i = 0; i < samples.length; i++) {

    let sample = Math.max(

      -1,

      Math.min(1, samples[i])

    )

    sample = sample < 0

      ? sample * 0x8000

      : sample * 0x7FFF

    view.setInt16(
      offset,
      sample,
      true
    )

    offset += 2

  }

  return new Blob(

    [view],

    {

      type: "audio/wav"

    }

  )

}