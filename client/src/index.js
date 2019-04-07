import React, { Component } from 'react';  // new
import ReactDOM from 'react-dom';
import axios from 'axios';

import Button from 'react-bootstrap/Button';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Container from 'react-bootstrap/Container';
import Spinner from 'react-bootstrap/Spinner';
import Tabs from 'react-bootstrap/Tabs';
import Tab from 'react-bootstrap/Tab';


// new
class App extends Component {
  constructor() {
    super();
    // new
    this.state = {
      loading: false,
      input: '',
      depth: 3,
      index_response: '',
      search_response: '',
      search_results: [],
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleIndexClick = this.handleIndexClick.bind(this);
    this.handleClearClick = this.handleClearClick.bind(this);
    this.handleSearchClick = this.handleSearchClick.bind(this);
    this.handleCheckbox = this.handleCheckbox.bind(this);
  };

  handleChange(event) {
    this.setState({input: event.target.value});
  };

  handleCheckbox(event) {
    this.setState({depth: event.target.value});
  };

  handleSearchClick(event) {
    event.preventDefault();

    this.setState({loading: true}, () => {
      axios.get(`${process.env.REACT_APP_BACKEND_URL}/search/?keyword=` + this.state.input)
          .then((res) => {var html = "Found " + res.data.number_of_results + ' results';
                                    this.setState({loading: false,
                                                          search_response: html,
                                                          search_results: res.data.search_results}); })
          .catch((err) => { console.log(err); });
    });
  };

  handleClearClick(event) {
    event.preventDefault();

    axios.get(`${process.env.REACT_APP_BACKEND_URL}/clear/`)
    .then((res) => { this.setState({index_response: res.data.message}); })
    .catch((err) => { console.log(err); });
  };

  handleIndexClick(event) {
    event.preventDefault();

    this.setState({loading: true}, () => {
      axios.get(`${process.env.REACT_APP_BACKEND_URL}/index/?url=` + this.state.input + '&depth=' + this.state.depth)
          .then((res) => {var html = "Indexed " + res.data.pages_crawled + ' pages and ' +
                                              res.data.words_found + " words";
                                    this.setState({loading: false,
                                                          index_response: html}); })
          .catch((err) => { console.log(err); });
    });
  };

  render() {
    const loading = this.state.loading;
    const index_response = this.state.index_response;
    const search_response = this.state.search_response;

    return (
       <Container>
         <h1>Simple Search Engine</h1>
         <Tabs defaultActiveKey="index" id="tabs">
           <Tab eventKey="search" title="Search" className="mt-4">
              <Form>
              <Row>
                <Col md={{ span: 8, offset: 2 }}>
                  <Form.Control placeholder="Enter word" onChange={this.handleChange}/>
                </Col>
              </Row>
              <Row className="text-center mt-3">
                <Col>
                  <Button variant="success" onClick={this.handleSearchClick}>Search</Button>
                </Col>
              </Row>
              <Row className="mt-4">
                <Col>
                  {loading ? <Spinner animation="border" /> : search_response}
                </Col>
              </Row>
              {
                this.state.search_results.map((result) => {
                  return (
                      <Row className="mt-3" key={result.url}>
                        <Col>
                          <a href={result.url} key={result.url} target="_blank">{result.title}</a><br/>
                          Occurrences: <b>{result.word_count}</b><br/>
                        </Col>
                      </Row>

                  )
                })
              }
            </Form>
           </Tab>
           <Tab eventKey="index" title="Index" className="mt-4">
            <Form>
              <Row>
                <Col md={{ span: 8, offset: 2 }}>
                  <Form.Control placeholder="Enter url" onChange={this.handleChange}/>
                </Col>
              </Row>
              <Row>
                <Col md={{ span: 8, offset: 2 }} className="mt-2">
                   Crawl Depth<br/>
                  <Form.Check inline label="1" value="1" type="radio" name="depth"
                              id="inline-radio-1" onChange={this.handleCheckbox}/>
                  <Form.Check inline label="2" value="2" type="radio" name="depth"
                              id="inline-radio-2" onChange={this.handleCheckbox} />
                  <Form.Check inline label="3" value="3" type="radio" name="depth"
                              id="inline-radio-3" onChange={this.handleCheckbox} defaultChecked />
                </Col>
              </Row>
              <Row className="text-center mt-2">
                <Col>
                  <Button variant="success" onClick={this.handleIndexClick}>Index</Button>
                  <Button variant="danger" className="ml-2" onClick={this.handleClearClick}>Clear</Button>
                </Col>
              </Row>
              <Row className="mt-4">
                <Col>
                  {loading ? <Spinner animation="border" /> : index_response}
                </Col>
              </Row>
            </Form>
           </Tab>
         </Tabs>
       </Container>
    )
  }
};

ReactDOM.render(
  <App />,
  document.getElementById('root')
);
