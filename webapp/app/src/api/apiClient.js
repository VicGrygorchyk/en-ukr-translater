
export class ApiClient {
   
    /**
     * 
     * @param {input: str; source_lang: 'en' | 'uk'} translateBody 
     * @return string
     */
    async translate(translateBody) {
        const response = await fetch('/translate', {
          method: 'POST',
          body: JSON.stringify(translateBody),
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
          },
        });
        console.log(response);
        const result = await response.json();
        const translated = result.map((text) => text.translation_text).join(' ');
        return translated;
    }
}
