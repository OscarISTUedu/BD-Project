function getCsrfToken() {
  let match = document.cookie.split('csrftoken=')[1]
  if (match) return match;
  return null;
}

function makeEditable(element) {
            if (user_group != "Пациенты")
            {
                const user_perm_arr_BD = user_perm.split(", ");
                const user_perm_arr = user_perm_arr_BD.map(item => item.split('.')[1]);
                model_dict = {
                    "Участки":"neighborhood",
                    "Пациенты":"patient",
                    "Цели визита":"visit",
                    "Врачи":"doctor",
                    "Талоны":"ticket",
                    "Диагнозы":"diagnosis"}
                if (user_perm.includes("change_"+model_dict[model]))
                {
                    old_value = element.innerText;
                    console.log("123 ",old_value);
                    console.log(123);
                    element.contentEditable = true;
                    element.focus();
                    element.onkeydown = function(event) {
                        if (event.key === 'Enter') {
                            element.contentEditable = false;
                            csrfToken = getCsrfToken();
                        let xhr = new XMLHttpRequest();
                        xhr.open("POST", "/change/", true);
                        xhr.setRequestHeader("Content-Type", "application/json");
                        xhr.setRequestHeader("X-CSRFToken", csrfToken);
                        parentElement = element.parentElement;
                        children = parentElement.children;
                        index = Array.prototype.indexOf.call(children, element);
                        thead = document.querySelector('thead').children[0];
                        field_name = thead.children[index].innerText;
                        let data = {
                          "table_verbose_name_plural": model,
                          "id": element.parentElement.firstElementChild.innerText,
                          "field_name":field_name,
                          "new_data":element.innerText,
                          "old_data":123,
                        };
                        let jsonData = JSON.stringify(data);
                        xhr.onload = function ()
                        {
                          if (xhr.status == 200) {
                          if (xhr.responseText!="")
                                {let response = {};
                                response = JSON.parse(xhr.responseText);}
                          } else {
                            console.error("Ошибка запроса: " + xhr.status);
                          }
                        };
                        xhr.send(jsonData);
                        }
                        }

                    element.onblur = function()
                    {
                        element.contentEditable = false;
                        csrfToken = getCsrfToken();
                        let xhr = new XMLHttpRequest();
                        xhr.open("POST", "/change/", true);
                        xhr.setRequestHeader("Content-Type", "application/json");
                        xhr.setRequestHeader("X-CSRFToken", csrfToken);
                        parentElement = element.parentElement;
                        children = parentElement.children;
                        index = Array.prototype.indexOf.call(children, element);
                        thead = document.querySelector('thead').children[0];
                        field_name = thead.children[index].innerText;
                        let data = {
                          "table_verbose_name_plural": model,
                          "id": element.parentElement.firstElementChild.innerText,
                          "field_name":field_name,
                          "new_data":element.innerText,
                        };
                        let jsonData = JSON.stringify(data);
                        xhr.onload = function ()
                        {
                          if (xhr.status == 200) {
                          if (xhr.responseText!="")
                                {let response = {};
                                response = JSON.parse(xhr.responseText);}
                          } else {
                            console.error("Ошибка запроса: " + xhr.status);
                          }
                        };
                        xhr.send(jsonData);
                    }
                }
            }
        }
