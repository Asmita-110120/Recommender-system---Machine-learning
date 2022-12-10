from flask import Flask,render_template,request
import pickle
import numpy as np

df = pickle.load(open('popular.pkl', 'rb'))
pivot = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_ = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(df['Book-Title'].values),
                           author=list(df['Book-Author'].values),
                           image=list(df['Image-URL-M'].values),
                           votes=list(df['num_ratings'].values),
                           rating=list(df['avg_rating'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index_ = np.where(pivot.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_[index_])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp = books[books['Book-Title'] == pivot.index[i[0]]]
        item.extend(list(temp.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)


if __name__ == '__main__':
    app.run(debug=True)