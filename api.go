package main

import (
	"github.com/kataras/iris"
	"io/ioutil"
	"sort"
	"github.com/kataras/iris/context"
	"log"
	"os/exec"
	"net/http"
)

func SetAPI(app iris.Party) {
	app.Get("/i/names", func(c context.Context) {
		files, err := ioutil.ReadDir(WORKSPACE)
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
		err := c.SendFile(WORKSPACE+name, "img.jpg")
		if err != nil {
			c.StatusCode(iris.StatusInternalServerError)
			c.JSON(iris.Map{"error": err.Error()})
		}
	})


	app.Get("/i/registration", func(c context.Context) {
		cmd := exec.Command("sh", "core/register_workspace.sh", WORKSPACE, REGISTRATION_FOLDER)
		log.Println(cmd.Args)
		out, err := cmd.Output()

		if err != nil {
			http.Error(c.ResponseWriter(), err.Error(), http.StatusInternalServerError)
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
		log.Println("err:", err)

		if err != nil {
			c.StatusCode(iris.StatusInternalServerError)
			c.JSON(iris.Map{"error": err.Error()})
		}

		name := string(out)

		err = c.SendFile(REGISTRATION_FOLDER+name, "img.jpg")

		log.Println(REGISTRATION_FOLDER+name)
		if err != nil {
			c.StatusCode(iris.StatusInternalServerError)
			c.JSON(iris.Map{"error": err.Error()})
		}
	})

}
