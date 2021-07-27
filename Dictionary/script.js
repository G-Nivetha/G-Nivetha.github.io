
function wordSearch() {
    var word = document.getElementById('searchBox').value;
    // call API get data
    if (word === '') {
        alert('Word is required');
        return;
    }
    getData(word);
}

async function getData(word) {
    const response = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${word}`);
    const data = await response.json();
    // if empty result 
    if (!data.length) {
        alert('No result found');
        return;
    } else {
        console.log(data[0].meanings)
        createData(data[0].phonetics, data[0].meanings)
    }
}

function createData(phonet, mean) {
    document.getElementById("accordion").innerHTML = `
    <input type="radio" name="select" class="accordion-select" />
            <div class="accordion-title"><span>Phonetics</span></div>
            <div class="accordion-content">
    <ul style="list-style-type: none;">
        ${phonet.map(phone => {
        return `<li>${phone.text}</li><br><li><audio controls style="outline: none;">
        <source src=${phone.audio} type="audio/mpeg">
        Your browser does not support the audio tag.
      </audio></li>`
    }).join('')}</ul></div>    

    ${mean.map(meaning => {
        return `<input type="radio" name="select" class="accordion-select" />
            <div class="accordion-title"><span>Part of Speech: ${meaning.partOfSpeech}</span></div>
            <div class="accordion-content"><ul style="list-style-type: none;">
            ${meaning.definitions.map(def => {
            if (!def.definition) {
                def.definition = '  -- --';
            }
            if (!def.example) {
                def.example = '  -- --';
            }
            if (!def.synonyms) {
                def.synonyms = '  -- --';
            }
            return `<li><b>Definition: </b>${def.definition}</li><br>
            <li><b>Example: </b>${def.example}</li><br>
            <li><b>Synonyms: </b>${def.synonyms}</li><br><br>`
        })}</ul></div> `
    }).join('')} `

}