function deleteMeal(mealId) {
  fetch("/delete-meal", {
    method: "POST",
    body: JSON.stringify({ mealId: mealId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteTag(tagId) {
  fetch("/delete-tag", {
    method: "POST",
    body: JSON.stringify({ tagId: tagId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}