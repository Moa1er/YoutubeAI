// Imports the Google Cloud client library
const textToSpeech = require('@google-cloud/text-to-speech');

// Import other required libraries
const fs = require('fs');
const util = require('util');
// Creates a client
const client = new textToSpeech.TextToSpeechClient();
async function quickStart() {
  // The text to synthesize
  const text = 'Roman history is a captivating tale of a civilization that spanned over a millennium, from its legendary foundation in 753 BCE to the fall of the Western Roman Empire in 476 CE. Rooted in the city of Rome, this ancient superpower grew to dominate the Mediterranean world and beyond. The Romans left an indelible mark on history through their innovations in governance, engineering, and law, as well as their military prowess. They are renowned for their iconic leaders, like Julius Caesar and Augustus, and their enduring architectural marvels, such as the Colosseum and the Roman Forum. Roman history is a story of conquest, cultural assimilation, and transformation, which continues to shape our understanding of the ancient world.';

  // Construct the request
  const request = {
    input: {text: text},
    // Select the language and SSML voice gender (optional)
    voice: {languageCode: 'en-US', ssmlGender: 'NEUTRAL'},
    // select the type of audio encoding
    audioConfig: {audioEncoding: 'MP3'},
  };

  // Performs the text-to-speech request
  const [response] = await client.synthesizeSpeech(request);
  // Write the binary audio content to a local file
  const writeFile = util.promisify(fs.writeFile);
  await writeFile('output.mp3', response.audioContent, 'binary');
  console.log('Audio content written to file: output.mp3');
}
quickStart();