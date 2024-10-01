## Custom Flask annotation app
In the context of a wildlife monitoring with computer vision project, this simple specimens image pairs annotation tool was developed using Flask and html. 

For installation:

```bash
git clone https://github.com/oriolus98/image_pairs_labeller.git
cd image_pairs_labeller

pip install -r requirements.txt
```

Images of specimens collected by expert environmentalists must be uploaded on static/images/
Then, the hole dataset can be divided between different expert annotators, each with its own login identification (defined in app.py), and the annotation app can be launched:

```bash
python distribute_pairs.py

python app.py
```

This app allows to identify and annotate if two different images belong to the same individual specimen, for posterior classification or instance recognition tasks:

<img align="center" src="./figs/app_example.png" width=1000 />

Future work: implement MongoDB database for larger image databases