var searchInput = document.getElementById("search");
        var searchButton = document.getElementById("search-button");
        var searchResults = document.getElementById("search-results");
        var userList = document.getElementById("user-list");
        console.log("in js")
    
        searchButton.addEventListener("click", function() {
            var searchTerm = searchInput.value;
                fetch("user/search/?q=" + searchTerm)
                    .then(response => response.json())
                    .then(data => {
                        if(data.length==0){
                            alert("")
                        }
                        else{
                        data.forEach(user => {

                            var existingRows = userList.querySelectorAll('tr');
                existingRows.forEach(row => {
                    var userNameCell = row.querySelector('td');
                    if (userNameCell && userNameCell.textContent.trim() === data[0].username) {
                        row.remove();
                    }
                });
                    
                            var userHtml = `<tr>
                                <td>${user.username}</td>
                                <td><input type="checkbox" class="form-check-input" name="selected_users" value="${user.id}" checked></td>
                            </tr>`;
                            userList.insertAdjacentHTML("afterbegin", userHtml);
                        
                        });
                    }
                })
            
        });