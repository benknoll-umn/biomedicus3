/*
 * Copyright 2019 Regents of the University of Minnesota
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package edu.umn.biomedicus.rtf.beans.keywords;

import edu.umn.biomedicus.rtf.exc.RtfReaderException;
import edu.umn.biomedicus.rtf.reader.KeywordAction;
import edu.umn.biomedicus.rtf.reader.RtfSink;
import edu.umn.biomedicus.rtf.reader.RtfSource;
import edu.umn.biomedicus.rtf.reader.State;

import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;
import java.io.IOException;

/**
 *
 */
@XmlRootElement
@XmlType
public class UnicodeKeywordAction extends AbstractKeywordAction {

  @Override
  public String executeAction(State state, RtfSource source, RtfSink sink) throws IOException {
    if (!hasParameter()) {
      throw new RtfReaderException("Unicode keyword without a parameter.");
    }
    sink.writeCharacter((char) getParameter(), getStartIndex(), getEnd());
    int charsToSkip = state.getPropertyValue("DocumentFormatting", "UnicodeByteCount") - 1;
    int read = source.read();
    if (read == ' ' || read == '\n' || read == '\r') {
      read = source.read();
    }


  }

  @Override
  public KeywordAction copy() {
    return new UnicodeKeywordAction();
  }
}