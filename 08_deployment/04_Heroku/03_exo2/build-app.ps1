	param (
	    [string]$Name
	)
	
	if (-not $Name) {
	    Write-Host "Veuillez fournir un nom d'application."
	    exit
	}
	
	# Remplacer les caractères non valides
	$ValidName = $Name -replace '_', '-'
	
	# Vérifier si le nom commence par une lettre
	if ($ValidName -match '^[^a-zA-Z]') {
	    Write-Host "Le nom doit commencer par une lettre. Modifiez le nom et réessayez."
	    exit
	}
	
	# Vérifier si le nom se termine par une lettre ou un chiffre
	if ($ValidName -match '[^a-zA-Z0-9]$') {
	    Write-Host "Le nom doit se terminer par une lettre ou un chiffre. Modifiez le nom et réessayez."
	    exit
	}
	
	
	# ./build_app.ps1 -Name demo-exo2 (pas de "_" mais si y en a un il sera remplacé)
	heroku container:login
	docker build -t $ValidName .
	heroku create $ValidName
	heroku container:push web -a $ValidName
	heroku container:release web -a $ValidName
	heroku open -a $ValidName
