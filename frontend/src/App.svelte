<script>
  let error = false;
  let lig = '';
  let urlField;
  let compName = '';
  let previewImg;

  async function onSubmit(e) {
    console.log(lig)
    if(lig == '' || compName == ''){
      console.log('no url')
      urlField.focus()
      error = true
    } else{
        var res = await fetch(`http://127.0.0.1:5000/yo/`, {
          method: 'POST',
          body: JSON.stringify({
            url: lig,
            name: compName
          }),
          headers: {
		        'Content-type': 'application/json; charset=UTF-8'
	        }
        })
        previewImg = lig;
        lig = '';
        compName = '';
        urlField.focus()
        //console.log(res.headers.get('Content-Disposition'))
    }
  }

  function typed(e){
    if(lig != '')
      error = false
    else error = true;  
  }

  async function batchProcess(e){
    if(!confirm('WARNING: this will probably take a while.'))
      return    
    console.log(await fetch('http://127.0.0.1:5000/yo/batch-process', {
      method: 'GET'
    }))
  }

  async function batchUpload(e){
    if(!confirm('WARNING: this will delete all imgs from postprocessed dir.'))
      return    
    console.log(await fetch('http://127.0.0.1:5000/yo/batch-upload', {
      method: 'GET'
    }))
  }

</script>

<main>
  <div class='container'>
    <div class="card" id='form'>
      <form on:submit|preventDefault={onSubmit}>
        <h3>url must end in extension(.png/.jpg/.etc)</h3>
        <input style="!important margin-bottom: 8px" bind:this={urlField} on:change={typed} bind:value={lig} name='lig' id='url' type='text' placeholder="enter image URL">
        <input on:change={typed} bind:value={compName} name='name' id='url' type='text' placeholder="enter company name">
          <div style="padding-top: 4%; padding-bottom: 4%; margin-top: 8%; margin-bottom: 8%;">
            {#if error}
            <p class="error-message">enter url & name</p>
            {/if}
          </div>       
        <button type='submit' style='margin-top: 0%'>download img</button>
        <br>
        <button on:click|preventDefault={batchProcess} style='margin-top: 30%; color: white; background-color: green;'>batch process</button>
        <button on:click|preventDefault={batchUpload} style='margin-top: 30%; color: white; background-color: red;'>batch upload</button>
      </form>
    </div>
    <div class="card" id='preview'>
      <img src={previewImg} style="width: 300px; height: auto;" alt="preview img" />
    </div>
  </div>
    
</main>

<style>
  .container{
    display: flex;
  }

  #form{
    padding-right: 500px;
    flex: 30%;
  }

  #preview{
    /* margin-left: 80%; */
    flex: 70%;
  }

  #url{
    padding: 10% 2% 10% 8%;
    margin-bottom: 25px;
    width: auto;
    font-size: large;
  }

  .error-message {
    color: tomato;
    font-size: 1.2em;
    margin: 0%;
    padding: 0;
  }

</style>
