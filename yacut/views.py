from urllib.parse import urljoin, urlparse

from flask import abort, flash, Markup, redirect, render_template, request

from . import app, db
from yacut.forms import LinkForm
from yacut.models import URLMap
from .validators import is_unique, latin_and_digits_length


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if form.validate_on_submit():
        if not is_unique(form.data.get('custom_id')):
            flash(f'Имя {form.data.get("custom_id")} уже занято!', 'not_unique_message')
            return render_template('index.html', form=form)
        if not latin_and_digits_length(form.data.get('custom_id')):
            flash('Указано недопустимое имя для короткой ссылки', 'not_appropriate_message')
            return render_template('index.html', form=form)
        url = URLMap()
        url.from_dict(form.data, 'original_link', 'custom_id')
        
            
        db.session.add(url)
        db.session.commit()
        domain = urlparse(request.base_url).scheme + '://' + urlparse(request.base_url).netloc
        new_link_message = flash(
            Markup(
            f'Ваша новая ссылка готова: <a href="{urljoin(domain, url.short)}"> {urljoin(domain, url.short)}</a>'),
            'new_link_message'
            )
        return render_template ('index.html', form = form) #new_link_message=new_link_message)
        repeat_message = flash(
                f'Имя {form.data["custom_id"]} уже занято!',
                'repeat_message'
                )
            
        
    return render_template('index.html', form = form)
    # abort(404)

@app.route('/<string:short>')
def redirect_to_original(short):
    url = URLMap.query.filter_by(short=short).first_or_404()
    print(url.id)
    return redirect (url.original)
