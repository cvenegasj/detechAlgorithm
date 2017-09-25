package main

import (
	"github.com/kataras/iris"
	"io/ioutil"
	"sort"
	"github.com/kataras/iris/context"
	"log"
	"os/exec"
	"fmt"
	"os"
)

func SetAPI(app iris.Party) {
	app.Get("/i/delete_all", func(c context.Context) {
		err := os.RemoveAll(UPLOAD_FOLDER)
		if err!=nil {
			log.Println(err)
			c.StatusCode(iris.StatusInternalServerError)
			c.JSON(iris.Map{

				"error": err.Error(),
			})
		}

		err = os.RemoveAll(WORKSPACE_FOLDER)
		if err!=nil {
			log.Println(err)

			c.StatusCode(iris.StatusInternalServerError)
			c.JSON(iris.Map{
				"error": err.Error(),
			})
		}

		err = os.RemoveAll(REGISTRATION_FOLDER)
		if err!=nil {
			log.Println(err)

			c.StatusCode(iris.StatusInternalServerError)
			c.JSON(iris.Map{
				"error": err.Error(),
			})
		}



		err = os.MkdirAll(UPLOAD_FOLDER,os.ModePerm)
		if err!=nil {
			log.Println(err)

			c.StatusCode(iris.StatusInternalServerError)
			c.JSON(iris.Map{
				"error": err.Error(),
			})
		}

		err = os.MkdirAll(WORKSPACE_FOLDER,os.ModePerm)
		if err!=nil {
			log.Println(err)

			c.StatusCode(iris.StatusInternalServerError)
			c.JSON(iris.Map{
				"error": err.Error(),
			})
		}

		err = os.MkdirAll(REGISTRATION_FOLDER,os.ModePerm)
		if err!=nil {
			log.Println(err)

			c.StatusCode(iris.StatusInternalServerError)
			c.JSON(iris.Map{
				"error": err.Error(),
			})
		}

	})

	app.Get("/i/names", func(c context.Context) {
		files, err := ioutil.ReadDir(WORKSPACE_FOLDER)
		if err != nil {
			c.StatusCode(iris.StatusInternalServerError)
			c.Err()
		}
		nameFiles := make([]string, 0)
		for _, file := range files {
			nameFiles = append(nameFiles, file.Name())
		}
		log.Println(nameFiles)
		sort.Sort(ByDetechTag(nameFiles))
		log.Println(nameFiles)

		c.StatusCode(iris.StatusOK)
		c.JSON(nameFiles)

	})


	app.Get("/i/{name}", func(c context.Context) {
		name := c.Params().Get("name")
		err := c.SendFile(WORKSPACE_FOLDER+name, "img.jpg")
		if err != nil {
			c.StatusCode(iris.StatusInternalServerError)
			c.JSON(iris.Map{"error": err.Error()})
		}
	})


	app.Get("/i/registration", func(c context.Context) {
		cmd := exec.Command("sh", "core/register_workspace.sh", WORKSPACE_FOLDER, REGISTRATION_FOLDER)
		log.Println(cmd.Args)
		out, err := cmd.Output()

		if err != nil {
			log.Println(err)
			c.StatusCode(iris.StatusInternalServerError)
			c.JSON(iris.Map{
				"error": err.Error(),
				"output": string(out),
			})
			return
		}
		c.StatusCode(iris.StatusOK)
		c.JSON(iris.Map{"output": out})

	})

	app.Get("/i/reg/{name}", func(c context.Context) {
		name := c.Params().Get("name")
		err := c.SendFile(REGISTRATION_FOLDER+name, "img.jpg")
		log.Println(REGISTRATION_FOLDER+name)
		if err != nil {
			c.StatusCode(iris.StatusInternalServerError)
			c.JSON(iris.Map{"error": err.Error()})
		}
	})

	app.Get("/i/mean", func(c context.Context) {
		cmd := exec.Command("sh", "core/get_mean_image.sh", REGISTRATION_FOLDER)
		log.Println(cmd.Args)
		out, err := cmd.Output()

		if err != nil {
			c.StatusCode(iris.StatusInternalServerError)
			c.JSON(iris.Map{"error": err.Error()})
			return
		}

		name := fmt.Sprintf("%s", out)
		c.StatusCode(iris.StatusOK)
		c.JSON(iris.Map{"image": name})

	})

}
