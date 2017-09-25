package main

import (
	"github.com/kataras/iris"
	"github.com/kataras/iris/context"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
	"strings"
	"time"
)

const UPLOAD_FOLDER = "/Users/bregy/WebstormProjects/detechAlgorithm/uploads/"
const WORKSPACE_FOLDER = "/Users/bregy/WebstormProjects/detechAlgorithm/workspace/"
const REGISTRATION_FOLDER = "/Users/bregy/WebstormProjects/detechAlgorithm/registered/"


func main() {
	app := iris.New()

	view := iris.HTML("./templates", ".html")
	view.Reload(true)
	app.RegisterView(view)

	app.Get("/", func(c context.Context) {
		c.View("index.html")
	})

	app.Post("/upload-folder", func(c context.Context) {
		t1 := time.Now()
		//parse the multipart form in the request
		err := c.Request().ParseMultipartForm(100000)
		if err != nil {
			http.Error(c.ResponseWriter(), err.Error(), http.StatusInternalServerError)
			return
		}

		m := c.Request().MultipartForm
		files := m.File["file"]
		numOfFiles := len(files)
		if numOfFiles > 0 {
			/*
				directoryName := strings.Split(files[0].Filename, "/")[0]
				LastFolderUsed = directoryName
				if _, err := os.Stat(UPLOAD_FOLDER + directoryName); os.IsNotExist(err) {
					err = os.Mkdir(UPLOAD_FOLDER + directoryName, os.ModePerm)
					if err != nil {
						http.Error(c.ResponseWriter(), err.Error(), http.StatusInternalServerError)
						return
					}
				}
			*/

			for i, _ := range files {
				files[i].Filename = strings.Split(files[i].Filename, "/")[1]

				if strings.Contains(files[i].Filename, "detechPhoto") {
					files[i].Filename = strings.Replace(files[i].Filename, "FALLA", "", -1)

					file, err := files[i].Open()
					defer file.Close()
					if err != nil {
						http.Error(c.ResponseWriter(), err.Error(), http.StatusInternalServerError)
						return
					}

					dst, err := os.Create(UPLOAD_FOLDER + files[i].Filename)
					defer dst.Close()
					if err != nil {
						http.Error(c.ResponseWriter(), err.Error(), http.StatusInternalServerError)
						return
					}

					if _, err := io.Copy(dst, file); err != nil {
						http.Error(c.ResponseWriter(), err.Error(), http.StatusInternalServerError)
						return
					}
				}


			}
		}

		t2 := time.Now()

		c.StatusCode(iris.StatusOK)
		c.Writef("Upload of %d files completed in %s\n", numOfFiles, t2.Sub(t1).String())
		log.Printf("Upload of %d files completed in %s", numOfFiles, t2.Sub(t1).String())

		cmd := exec.Command("sh", "core/create_workspace.sh", UPLOAD_FOLDER, WORKSPACE_FOLDER)
		log.Println(cmd.Args)
		out, err := cmd.Output()
		if err != nil {
			http.Error(c.ResponseWriter(), err.Error(), http.StatusInternalServerError)
			return
		}
		log.Printf("Output: %s", out)

	})

	api := app.Party("/api")
	SetAPI(api)

	app.Run(iris.Addr(":8080"), iris.WithoutServerError(iris.ErrServerClosed))
}
