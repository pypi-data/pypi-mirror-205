python3 -m build

python3 -m twine check dist/*

python3 -m twine upload --verbose dist/ankitrazorpay-0.1-py3-none-any.whl dist/ankitrazorpay-0.1.tar.gz

python3 -m twine upload --verbose --repository testpypi dist/ankitrazorpay-0.1-py3-none-any.whl dist/ankitrazorpay-0.1.tar.gz

      - name: Set up Python 3
        uses: actions/setup-python@v2
        with:
          python-version: "3.10"


- name: Install tools
        run: make venv
      - name: Publish packages to PyPy
        run: |
          set -ex
          source venv/bin/activate
          export VERSION=$(cat VERSION)
          gpg --detach-sign --local-user $GPG_SIGNING_KEYID  --pinentry-mode loopback --passphrase $GPG_SIGNING_PASSPHRASE -a dist/stripe-$VERSION.tar.gz
          gpg --detach-sign --local-user $GPG_SIGNING_KEYID  --pinentry-mode loopback --passphrase $GPG_SIGNING_PASSPHRASE -a dist/stripe-$VERSION-py2.py3-none-any.whl
          python -m twine upload --verbose dist/stripe-$VERSION.tar.gz  dist/stripe-$VERSION-py2.py3-none-any.whl dist/stripe-$VERSION.tar.gz.asc dist/stripe-$VERSION-py2.py3-none-any.whl.asc
        env:
          GPG_SIGNING_KEYID: ${{ secrets.GPG_SIGNING_KEYID }}
          TWINE_USERNAME: ${{ secrets.TWINE_USERNAME }}
          TWINE_PASSWORD: ${{ secrets.TWINE_PASSWORD }}
          GPG_SIGNING_PASSPHRASE: ${{ secrets.GPG_SIGNING_PASSPHRASE }}
      - uses: stripe/openapi/actions/notify-release@master
        if: always()
        with:
          bot_token: ${{ secrets.SLACK_BOT_TOKEN }}
