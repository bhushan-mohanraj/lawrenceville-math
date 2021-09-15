# Static Files

- Download the Bootstrap source and move it to `app/static/bootstrap-x.y.z` where `x.y.z` is the Bootstrap version.
  - Add this folder to `.gitignore`.
  - Update the version to `x.y.z` in `app/static/scss/custom.scss`.
- Use SASS to convert `app/static/scss/custom.scss` to `app/static/css/bootstrap.css`.

```
sass app/static/scss/custom.scss app/static/css/bootstrap.css
```
