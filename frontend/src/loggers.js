/*
 * A common function to manage error from axios in its catch method
 *
 * errorStore: An object of errors, cloned to be used depending error issue,
 * it may be replaced with returned response body (that must be a JSON object)
 * from an http400 that is the way to return backend form errors. For every
 * other error kind an error message is pushed to array 'errorObject._global'.
 *
 * errorObject: Error object returned by axios.
 */
export function error_logger(errorStore, errorObject){
    var current_errors = errorStore;

    if (errorObject.response) {
        console.log("http %s", errorObject.response.status);

        if(errorObject.response.status == 400) {
            console.log("Error returned from form");
            current_errors = errorObject.response.data.data;
        } else if (errorObject.response.status == 500) {
            console.log("Error server");
            current_errors._global.push("Internal Server Error");
        } else if (errorObject.response.status == 404) {
            current_errors._global.push("Not Found");
        } else {
            console.log("Undetermined error");
            current_errors._global.push(`Error http${errorObject.response.status} : ${errorObject.response.statusText}`);
        }
    } else if (errorObject.request) {
        // The request was made but no response was received
        console.log("Request error");
        //console.log(errorObject.request);
        current_errors._global.push("Unable to send request to server");
    } else {
        // Something happened in setting up the request that triggered an Error
        console.log('Error', errorObject.message);
    }

    return current_errors;
}
