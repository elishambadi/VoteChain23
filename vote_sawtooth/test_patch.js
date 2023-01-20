#!/usr/bin/node

let PatchRequest = () => {
          // sending PUT request with fetch API in javascript
          fetch("http://localhost:8080/election/end", {
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json"
            },
            method: "PATCH",     
          
            // Fields that to be updated are passed
            body: JSON.stringify({
              name: "{ election[0]['name'] }}"
            })
          })
            .then(function (response) {
          
              // console.log(response);
              return response.json();
            })
            .then(function (data) {
              console.log(data);
            });
        };
          
        PatchRequest();
